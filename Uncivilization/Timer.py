import time

class Timer:
    def __init__(self):
        self.object_t0 = time.time()
        self.current_t0 = None
        self.paused_time = 0
        self.paused_t0 = None
        self.is_paused = False
        self.inactive = True
    
    def start_timer(self):
        if self.current_t0:
            print("Timer already started")
        
        if self.is_paused:
            print("Cannot start paused timer")

        if self.is_paused is False and self.current_t0 is None: 
            print("starting timer")
            self.current_t0 = time.time()
            self.inactive = False

    def end_timer(self):
        if self.inactive:
            print("Cannot end an inactive timer")
        
        dt = None

        if self.is_paused:
            self.resume_timer()
            print("Timer paused, resuming then ending")

        if self.current_t0:
            dt = time.time() - self.current_t0 - self.paused_time
            self.current_t0 = None
            self.paused_time = 0
            self.inactive = True
            print("ending timer")
        return dt
    
    def pause_timer(self):
        if self.is_paused:
            print("Timer is already Paused")
        
        if self.inactive:
            print("Cannot pause inactive timer")
        
        if not self.is_paused and not self.inactive:
            self.paused_t0 = time.time()
            self.is_paused = True
            print("Pausing timer")

    
    def resume_timer(self):
        if not self.is_paused:
            print("Can only resume a paused timer")
        
        if self.inactive:
            print("cannot resume an inactive timer")

        if self.is_paused and not self.inactive:
            self.paused_time += time.time() - self.paused_t0
            self.is_paused = False
            self.paused_t0 = None
            print("Resuming Timer")
    
    def peek_timer(self):
        dt = time.time() - self.current_t0 - self.paused_time if self.current_t0 is not None else None
        dt2 = time.time() - self.paused_t0 if self.paused_t0 is not None else None
        return dt,dt2
    
    def get_obj_lifetime(self):
        return time.time() - self.object_t0
