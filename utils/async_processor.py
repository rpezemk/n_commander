import threading

class AsyncProcessor():
    def __init__(self, non_ui_tasks: list):
        self.non_ui_tasks = non_ui_tasks
        self.threads = []
        self.threads = [threading.Thread(target=t) for t in self.non_ui_tasks]
        self.is_running = False
        
           
    def start(self):
        for t in self.threads:
            t.start()
                        
    def wait_for_me(self):
        self.is_running = True
        for t in self.threads:
            t.join()
        return self
        