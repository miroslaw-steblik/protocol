import luigi
import pandas as pd

class DownloadData(luigi.Task):
    def output(self):
        return luigi.LocalTarget('data.csv')

    def run(self):
        # Simulate downloading data
        data = {'column1': [1, 2, 3], 'column2': [4, 5, 6]}
        df = pd.DataFrame(data)
        df.to_csv(self.output().path, index=False)

class ProcessData(luigi.Task):
    def requires(self):
        return DownloadData()

    def output(self):
        return luigi.LocalTarget('processed_data.csv')

    def run(self):
        # Read the downloaded data
        df = pd.read_csv(self.input().path)
        # Simulate data processing
        df['column3'] = df['column1'] + df['column2']
        df.to_csv(self.output().path, index=False)

class SummarizeData(luigi.Task):
    def requires(self):
        return ProcessData()

    def output(self):
        return luigi.LocalTarget('summary.txt')

    def run(self):
        # Read the processed data
        df = pd.read_csv(self.input().path)
        # Simulate summarizing data
        summary = df.describe().to_string()
        with self.output().open('w') as f:
            f.write(summary)

if __name__ == '__main__':
    luigi.run()