"""
PLAN:
    1. Load data
    2. Data preprocessing
        - rename column names
        - rename questions into categories
    3. Melt dataframe
    4. Check for outliers
        - adjust outliers to the mean
    5. Pivot dataframe
    6. Data analysis
    7. Output formatting
"""


using DataFrames
using JSON
using Statistics
using Printf
using Query
using ShiftedArrays
using Profile


data_file = "/home/miros/DataOps/developer/white/protocol/data/raw_data.json"
clean_file = "/home/miros/DataOps/developer/white/protocol/data/clean_data.json"

cols_ordered = [
    "Project",
    "Question level 1",
    "Question level 2",
    "Question level 3",
    "Response 1",
    "Response 2",
    "Response 3",
    "Response 4",
    "Response 5"
]
# benchmarking

function load_data(data_file)
    data = read(data_file, String)
    data = replace(data, "'" => "\"")
    write(clean_file, data)
    df = DataFrame(JSON.parsefile(clean_file))
    return df
end

function process_data(df)
    df = df[:, cols_ordered]
    # Create a mapping from response columns to the first row values
    first_row = collect(df[1, :])
    columns = names(df)
    response_columns = filter(col -> occursin("Response", col), columns)
    column_map = Dict(col => first_row[findfirst(==(col), columns)] for col in response_columns)
    rename!(df, column_map)
    df = df[2:end, :]

    # Add year and period description columns
    df.Year = map(x -> split(x, " ")[end], df."Question level 2")
    df.Year = parse.(Int, df.Year)
    df.Period = map(x -> split(x, " ")[1], df."Question level 2")
    # Reset the index and drop unnecessary columns
    df = df[df."Question level 2" .!= "EoY 2024", :]
    select!(df, Not([:Project, Symbol("Question level 2")]))
    rename!(df, Symbol("Question level 1") => :Category, 
            Symbol("Question level 3") => :Subcategory)

    replacement_dict = Dict(
        "What was your AuM split over the last 5 years?" => "AUM Split",
        "What was your revenue in the last 5 years?"=> "Revenue",
        "What was your total AuM in the last 5 years?"=> "AUM"
    )
    df.Category = map(x -> replacement_dict[x], df.Category)

    # Convert to numeric, handling empty strings
    columns_num = ["Company A", "Company B", "Company C", "Company D", "Company E"]
    for col in columns_num
        df[!, col] = parse.(Float64, replace(df[!, col], "" => "NaN"))
    end

    df.Metric = df.Category .* "_" .* df.Subcategory
    return df, columns_num
end

    #------------------- MELT THE DATAFRAME -------------------#
function melt_data(df, columns_num)    
    df_melted = stack(df, columns_num, variable_name=:Company, value_name=:Value)
    df_melted = dropmissing(df_melted)
    df_melted = df_melted[.!isnan.(df_melted.Value), :]
    return df_melted
end

    #---------------------------- OUTLIERS -------------------#
function find_outliers(df)

    # Calculate the z-score and find outliers
    threshold = 1.75

    # Function to calculate z-scores
    function zscore(arr)
        μ = mean(arr)
        σ = std(arr)
        return (arr .- μ) ./ σ
    end

    # Calculate z-scores and adjust outliers to the mean
    df_outliers = combine(groupby(df, [:Company, :Metric])) do group
        group.z_score = abs.(zscore(group.Value))
        group.outlier = group.z_score .> threshold
        non_outlier_mean = mean(group.Value[.!group.outlier])
        group.Adjusted_Value = copy(group.Value)
        group[findall(group.outlier), :Adjusted_Value] .= non_outlier_mean
        return group
    end

    # println("\nDataFrame after adjusting outliers to the mean:")
    # println(df_outliers)
    return df_outliers
end

    # ------------------------ PIVOTING ------------------ #
function pivot_data(df)
    df_pivot = unstack(df, [:Company, :Year], :Metric, :Adjusted_Value)

    # Rename columns
    rename!(df_pivot, Dict(
        "AUM Split_Fixed income" => :AUM_FI,
        "AUM Split_Hedge funds" => :AUM_HF,
        "AUM Split_Multi-asset" => :AUM_MA,
        "AUM Split_Other" => :AUM_Other,
        "AUM Split_Private Debt" => :AUM_PD,
        "AUM Split_Private Equity" => :AUM_PE,
        "AUM Split_Public equities" => :AUM_PubEq,
        "Revenue_Total" => :Revenue,
        "AUM_Total" => :AUM
    ))
    return df_pivot
end
    # ------------------------ DATA ANALYSIS ------------------ #
function analyze_data(df_pivot)
    df_pivot.Revenue = df_pivot.Revenue ./ 1000

    sum_columns = [
        :AUM_FI, :AUM_HF, :AUM_MA, :AUM_Other, :AUM_PD, :AUM_PE, :AUM_PubEq
    ]
    # Calculate the total AUM
    df_pivot.AUM_Calculated = reduce(+, eachcol(select(df_pivot, sum_columns)))
    # Check if the calculated AUM matches the reported AUM
    df_pivot.AUM_Check = ifelse.(coalesce.(df_pivot.AUM, 0) .== coalesce.(df_pivot.AUM_Calculated, 0), "True", "False")

    df_pivot.AUM_PE_pct = df_pivot.AUM_PE ./ df_pivot.AUM_Calculated
    df_pivot.AUM_HF_pct = df_pivot.AUM_HF ./ df_pivot.AUM_Calculated

    #df_pivot.AUM_4Y_CAGR_ = ((coalesce.(df_pivot.AUM_Calculated, 0) ./ lag(coalesce.(df_pivot.AUM_Calculated, 0), 4)) .^ (1/4)) .- 1
    #df_pivot.Revenue_4Y_CAGR_ = ((coalesce.(df_pivot.Revenue, 0) ./ lag(coalesce.(df_pivot.Revenue, 0), 4)) .^ (1/4)) .- 1
 
end

    # ------------------------ OUTPUT ------------------ #
function generate_summary_table(df_pivot)    
    latest_year = maximum(df_pivot.Year)
    summary_table = df_pivot[df_pivot.Year .== latest_year, :]

    # format the output
    summary_table = select(summary_table, [:Company, :AUM_Calculated, :AUM_PE_pct, :AUM_HF_pct, :Revenue])
    rename!(summary_table, :AUM_PE_pct => "% PE in AUM")
    rename!(summary_table, :AUM_Calculated => "AUM (in millions)")
    rename!(summary_table, :AUM_HF_pct => "% HF in AUM")
    rename!(summary_table, :Revenue => "Revenue (in millions)")

    summary_table[!, "AUM (in millions)"]       = [@sprintf("%.0f", x) for x in summary_table[!, "AUM (in millions)"]]
    summary_table[!, "% PE in AUM"]             = [@sprintf("%.2f%%", x * 100) for x in summary_table[!, "% PE in AUM"]]
    summary_table[!, "% HF in AUM"]             = [@sprintf("%.2f%%", x * 100) for x in summary_table[!, "% HF in AUM"]]
    summary_table[!, "Revenue (in millions)"]   = [@sprintf("%.1f", x) for x in summary_table[!, "Revenue (in millions)"]]
    println("\nSummary table:")
    println(summary_table)
    return summary_table
end

# @time begin
#     Profile.clear()
#     @profile main()
#     Profile.print()
# end

# Main function
function main()
    df = load_data(data_file)
    df, columns_num = process_data(df)
    df_melted = melt_data(df, columns_num)
    df_outliers = find_outliers(df_melted)
    df_pivot = pivot_data(df_outliers)
    analyze_data(df_pivot)
    summary_table = generate_summary_table(df_pivot)
    return summary_table
end


@time main()



