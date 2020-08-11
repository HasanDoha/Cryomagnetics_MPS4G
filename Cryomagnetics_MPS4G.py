from VISA_Driver import VISA_Driver
import time


class Driver(VISA_Driver):
    """ This class re-implements the VISA driver"""

    def performOpen(self, options={}):
        """Perform the operation of opening the instrument connection"""
        # keep track of sweep state
        self.is_sweeping = False
        # calling the generic VISA open to make sure we have a connection
        VISA_Driver.performOpen(self, options=options)
        # do additional initialization code here...
        pass

    def performClose(self, bError=False, options={}):
        """Perform the close instrument connection operation"""
        # calling the generic VISA class to close communication
        VISA_Driver.performClose(self, bError, options=options)
        # do additional cleaning up code here...
        pass

    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation"""
        # for all other cases, call generic VISA driver
        if quant.name == 'B':
            instantB = 'IOUT?'
            instantB = self.askAndLog(instantB, bCheckError=True)
            instantB = instantB.replace('kG', '')
            instantB = float(instantB) / 0.01 #converting kGauss to mT
            value = instantB
        elif quant.name == 'Upper Sweep Limit':
            USL = 'ULIM?'
            USL = self.askAndLog(USL, bCheckError=True)
            USL = USL.replace('kG', '')
            USL = float(USL) / 0.01 #converting kGauss to mT
            value = USL
        elif quant.name == 'Lower Sweep Limit':
            LSL = 'LLIM?'
            LSL = self.askAndLog(LSL, bCheckError=True)
            LSL = LSL.replace('kG', '')
            LSL = float(LSL) / 0.01 #converting kGauss to mT
            value = LSL
        else:
            # otherwise, call standard VISA case
            value = VISA_Driver.performGetValue(self, quant, options)
        return value

    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation. This function should
        return the actual value set by the instrument"""
        if quant.name == 'B':
            givenBmT = float(value)
            givenB = givenBmT * 0.01	#converting mT to kGauss
            strGivenB = str(givenB)
            MaxUSL = float(85)
            MaxUSLmT = float(8500)
            strMaxUSL = str(MaxUSL)
            MaxLSL = float(-85)
            MaxLSLmT = float(-8500)
            strMaxLSL = str(MaxLSL)
            if sweepRate == True:
                maxSweepRate = 0.0400
                if sweepRate > maxSweepRate:
                    sweepRate = maxSweepRate
                strSweepRate = str(sweepRate)
                for i in range(0, 5):
                    Rate = 'RATE ' + str(i) + ' ' + strSweepRate
                    Rate = self.writeAndLog(Rate, bCheckError=True)
            elif sweepRate == False:
                maxSweepRate0 = 0.0400
                maxSweepRate1 = 0.0400
                maxSweepRate2 = 0.0400
                maxSweepRate3 = 0.0400
                maxSweepRate4 = 0.0120
                sweepRate0 = maxSweepRate0
                strSweepRate0 = str(sweepRate0)
                Rate0 = 'RATE 0 ' + strSweepRate0
                Rate0 = self.writeAndLog(Rate0, bCheckError=True)
                sweepRate1 = maxSweepRate1
                strSweepRate1 = str(sweepRate1)
                Rate1 = 'RATE 1 ' + strSweepRate1
                Rate1 = self.writeAndLog(Rate1, bCheckError=True)
                sweepRate2 = maxSweepRate2
                strSweepRate2 = str(sweepRate2)
                Rate2 = 'RATE 2 ' + strSweepRate2
                Rate2 = self.writeAndLog(Rate2, bCheckError=True)
                sweepRate3 = maxSweepRate3
                strSweepRate3 = str(sweepRate3)
                Rate3 = 'RATE 3 ' + strSweepRate3
                Rate3 = self.writeAndLog(Rate3, bCheckError=True)
                sweepRate4 = 0.0120
                sweepRate4 = maxSweepRate4
                strSweepRate4 = str(sweepRate4)
                Rate4 = 'RATE 4' + strSweepRate4
                Rate4 = self.writeAndLog(Rate4, bCheckError=True)
            SwitchHeater = 'PSHTR?'
            SwitchHeater = int(self.askAndLog(SwitchHeater, bCheckError=True))
            if SwitchHeater == 0:
                SwitchHeater = 'PSHTR ON'
                SwitchHeater = self.writeAndLog(SwitchHeater, bCheckError=True)
                time.sleep(300)	#wait for 300 seconds = 5 minutes
            if givenB>=0.0 and givenB<=MaxUSL:
                SetUSL = self.sendValueToOther('Upper Sweep Limit', givenBmT)
                SweepStart = quant.sweep_cmd.replace('<sr>',' UP')
                SweepStart = self.writeAndLog(SweepStart, bCheckError=True)
            elif givenB>=0.0 and givenB>MaxUSL:
                SetUSL = self.sendValueToOther('Upper Sweep Limit', MaxUSLmT)
                SweepStart = quant.sweep_cmd.replace('<sr>',' UP')
                SweepStart = self.writeAndLog(SweepStart, bCheckError=True)
            elif givenB<0.0 and givenB>=MaxLSL:
                SetLSL = self.sendValueToOther('Lower Sweep Limit', givenBmT)
                SweepStart = quant.sweep_cmd.replace('<sr>',' DOWN')
                SweepStart = self.writeAndLog(SweepStart, bCheckError=True)
            elif givenB<0.0 and givenB<MaxLSL:
                SetLSL = self.sendValueToOther('Lower Sweep Limit', MaxLSLmT)
                SweepStart = quant.sweep_cmd.replace('<sr>',' DOWN')
                SweepStart = self.writeAndLog(SweepStart, bCheckError=True)
            return value
        elif quant.name == 'Upper Sweep Limit':
            givenUSL = float(value)
            givenUSL = givenUSL * 0.01	#converting mT to kGauss
            strGivenUSL = str(givenUSL)
            USL = 'ULIM ' + strGivenUSL
            USL = self.writeAndLog(USL, bCheckError=True)
            return value
        elif quant.name == 'Lower Sweep Limit':
            givenLSL = float(value)
            givenLSL = givenLSL * 0.01	#converting mT to kGauss
            strGivenLSL = str(givenLSL)
            LSL = 'LLIM ' + strGivenLSL
            LSL = self.writeAndLog(LSL, bCheckError=True)
            return value
        else:
            # otherwise, call standard VISA case
            value = VISA_Driver.performSetValue(self, quant, value, sweepRate, options)
        return value

    def checkIfSweeping(self, quant, options={}):
        """Check if instrument is sweeping the given quantity"""
        status = self.readValueFromOther('Sweep')
        USL = self.readValueFromOther('Upper Sweep Limit')
        USL = float(USL)
        LSL = self.readValueFromOther('Lower Sweep Limit')
        LSL = float(LSL)
        instantB = 'IOUT?'
        instantB = self.askAndLog(instantB, bCheckError=True)
        instantB = instantB.replace('kG', '')
        instantB = float(instantB) / 0.01	#converting kGauss to mT
        if (status == 'Sweeping up' and instantB == USL):
            self.is_sweeping = False
        elif (status == 'Sweeping up' and instantB < USL):
            self.is_sweeping = True
        elif (status == 'Sweeping up' and instantB > USL):
            self.is_sweeping = True
        elif (status == 'Sweeping down' and instantB == LSL):
            self.is_sweeping = False
        elif (status == 'Sweeping down' and instantB > LSL):
            self.is_sweeping = True
        elif (status == 'Sweeping down' and instantB < LSL):
            self.is_sweeping = True
        return self.is_sweeping
