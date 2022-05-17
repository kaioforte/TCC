import win32com.client


class DSS():

    def __init__(self, filepath):

        self.filepath = filepath
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

        if self.dssObj.Start(0) is False:
            print('Problema ao iniciar o OpenDSS')

        else:
            self.DSSText = self.dssObj.Text
            self.DSSCircuit = self.dssObj.ActiveCircuit
            self.DSSSolution = self.DSSCircuit.Solution
            self.DSSCktElement = self.DSSCircuit.ActiveElement
            self.DSSBus = self.DSSCircuit.ActiveBus
            self.DSSLines = self.DSSCircuit.Lines
            self.DSSTransformers = self.DSSCircuit.Transformers
            self.DSSPVSystems = self.DSSCircuit.PVSystems
            self.DSSMeters = self.DSSCircuit.Meters
            self.DSSLoads = self.DSSCircuit.Loads
            self.DSSActiveBus = self.DSSCircuit.ActiveBus
            self.DSSXfmr = self.DSSCircuit.Transformers

    def compile(self):

        self.dssObj.ClearAll()
        self.DSSText.Command = "compile " + self.filepath

    def solve(self):

        self.DSSText.Command = "Set Mode=SnapShot"
        self.DSSText.Command = "Set ControlMode=Static"
        self.DSSSolution.Solve()
