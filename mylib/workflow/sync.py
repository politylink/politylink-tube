from mylib.workflow.models import BashOperator


class SyncDirJob(BashOperator):
    def __init__(self, src_dir: str, dest_dir: str):
        context = self.init_context(locals())

        bash_command = f"rsync -a -v --exclude '*.wav' --exclude '*.mp3' --exclude '*.mp4' {src_dir} {dest_dir}"

        super().__init__(bash_command=bash_command, context=context)


class SyncFileJob(BashOperator):
    def __init__(self, src_file: str, dest_file: str):
        context = self.init_context(locals())

        bash_command = f"scp {src_file} {dest_file}"

        super().__init__(bash_command=bash_command, context=context)
