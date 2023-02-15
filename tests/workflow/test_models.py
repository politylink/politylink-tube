from mylib.workflow.models import PythonOperator


class ExamplePythonJob(PythonOperator):
    def __init__(self, greeting, name):
        context = self.init_context(locals())

        def main():
            print(f'{greeting} {name}')

        super().__init__(main, context=context)


class TestPythonOperator:
    def test_context(self):
        job = ExamplePythonJob(greeting='hello', name='python')

        assert job.context.class_name == 'ExamplePythonJob'
        assert len(job.context.class_kwargs) == 2
        assert job.context.class_kwargs['greeting'] == 'hello'
        assert job.context.class_kwargs['name'] == 'python'
