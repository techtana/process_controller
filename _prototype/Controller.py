class Controller:
    def __init__(self):
        self.state = 0 
        self.recommend = 0
        self._records = list()
        self._n_records = 5
        self._alpha = 0.5
        self._lambda = 0.5
        self.model = 1
        
    def update_measurement(self, meas):
        if len(self._records) == self._n_records:
            self._records.pop(0)
            self._records.append(meas)
        self.update_state()
        self.recommend()
    
    def update_state(self):
        self.state = self._alpha*self._records[-1] + (1-self._alpha)*self.state
        
    def recommend(self):
        self.recommend = (self._records[-1] - self.state)*self.model*self._lambda
    
    