import apache_beam as beam


def run():
    with beam.Pipeline() as pipeline:
        print('Hello World!')
        # Add your pipeline logic here
        pass

if __name__ == '__main__':
  run()