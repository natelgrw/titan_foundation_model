from eval_engines.spectre.core import EvaluationEngine
import numpy as np
import pdb
import IPython
import scipy.interpolate as interp
import scipy.optimize as sciopt
import scipy.integrate as scint
import matplotlib.pyplot as plt
import globalsy

class OpampMeasMan(EvaluationEngine):

    def __init__(self, yaml_fname):
        EvaluationEngine.__init__(self, yaml_fname)

    def get_specs(self, results_dict, params):
        print("Results dict keys:", results_dict.keys())
        specs_dict = dict()
        ac_dc = results_dict['ac_dc']
        for _, res, _ in ac_dc:
            specs_dict = res
        return specs_dict

    def compute_penalty(self, spec_nums, spec_kwrd):
        if type(spec_nums) is not list:
            spec_nums = [spec_nums]
        penalties = []
        for spec_num in spec_nums:
            penalty = 0
            spec_min, spec_max, w = self.spec_range[spec_kwrd]
            if spec_max is not None:
                if spec_num > spec_max:
                    penalty += w * abs(spec_num - spec_max) / abs(spec_num)
            if spec_min is not None:
                if spec_num < spec_min:
                    penalty += w * abs(spec_num - spec_min) / abs(spec_min)
            penalties.append(penalty)
        return penalties

class ACTB(object):

    @classmethod
    def process_ac(self, results, params):

        ac_result_diff = results['acswp-000_ac']
        ac_result_cm = results['acswp-001_ac']

        dc_results = results['dcswp-500_dcOp']

        noise_results = results["noise"]

        tran_results = results["tran_voutp"]

        vcm = dc_results["cm"]

        vout_diff = ac_result_diff['Voutp']
        freq = ac_result_diff['sweep_values']

        ids_MM = []
        gm_MM = []
        vgs_MM = []
        vds_MM = []
        region_MM = []

        for comp, val in dc_results.items():
            if comp.startswith("MM") and comp.endswith("ids"):
                ids_MM.append(float('%.3g' % np.abs(val)))
            elif comp.startswith("MM") and comp.endswith("gm"):
                gm_MM.append(float('%.3g' % np.abs(val)))
            elif comp.startswith("MM") and comp.endswith("vgs"):
                vgs_MM.append(float('%.3g' % np.abs(val)))
            elif comp.startswith("MM") and comp.endswith("vds"):
                vds_MM.append(float('%.3g' % np.abs(val)))
            elif comp.startswith("MM") and comp.endswith("region"):
                region_MM.append(float('%.3g' % np.abs(val)))

        vos = self.find_vos(results, vcm)
        gain = self.find_dc_gain(vout_diff)
        ugbw, valid = self.find_ugbw(freq, vout_diff)
        phm = self.find_phm(freq, vout_diff)
        power = -dc_results['V0:p']
        cmrr = self.find_cmrr(vout_diff, ac_result_cm['Voutp'])
        linearity = self.find_linearity(results, vout_diff)
        output_voltage_swing = self.find_output_voltage_swing(results, vcm)
        integrated_noise = self.find_integrated_noise(noise_results)
        slew_rate = self.find_slew_rate(tran_results)
        settle_time = self.find_settle_time(tran_results)

        if globalsy.counterrrr < 200:
                with open("/homes/natelgrw/Documents/titan_foundation_model/results/out1.txt",'a') as f:
                    print("metrics-", "gain: ", f'{float(gain):.5}', 
                        ", UGBW: ",  f'{float(ugbw):.5}', 
                        ", PM: ",  f'{float(phm):.5}', 
                        ", power: ", f'{float(power):.5}',
                        ", CMRR: ", f'{float(cmrr):.5}', 
                        ", Vos: ", f'{float(vos):.5}', 
                        ", linearity: ", f'{linearity}',
                        ", output_voltage_swing: ", f'{output_voltage_swing}',
                        ", integrated_noise: ", f'{integrated_noise:.5e}',
                        ", slew_rate: ", f'{slew_rate:.5e}',
                        ", settle_time: ", f'{settle_time:.5e}', valid, file=f)
        elif globalsy.counterrrr < 1200:
                with open("/homes/natelgrw/Documents/titan_foundation_model/results/out11.txt",'a') as f:
                    print("metrics-", "gain: ", f'{float(gain):.5}',
                        ", UGBW: ",  f'{float(ugbw):.5}', 
                        ", PM: ",  f'{float(phm):.5}', 
                        ", power: ", f'{float(power):.5}', 
                        ", CMRR: ", f'{float(cmrr):.5}',
                        ", Vos: ", f'{float(vos):.5}',
                        ", linearity: ", f'{linearity}',
                        ", output_voltage_swing: ", f'{output_voltage_swing}',
                        ", integrated_noise: ", f'{integrated_noise:.5e}',
                        ", slew_rate: ", f'{slew_rate:.5e}',
                        ", settle_time: ", f'{settle_time:.5e}', valid, file=f)
        elif globalsy.counterrrr < 2000:
                with open("/homes/natelgrw/Documents/titan_foundation_model/results/out12.txt",'a') as f:
                    print("metrics-", "gain: ", f'{float(gain):.5}', 
                        ", UGBW: ",  f'{float(ugbw):.5}', 
                        ", PM: ",  f'{float(phm):.5}', 
                        ", power: ", f'{float(power):.5}', 
                        ", CMRR: ", f'{float(cmrr):.5}',
                        ", Vos: ", f'{float(vos):.5}',
                        ", linearity: ", f'{linearity}',
                        ", output_voltage_swing: ", f'{output_voltage_swing}',
                        ", integrated_noise: ", f'{integrated_noise:.5e}',
                        ", slew_rate: ", f'{slew_rate:.5e}',
                        ", settle_time: ", f'{settle_time:.5e}', valid, file=f)

        results = dict(
            gain = gain,
            funity = ugbw,
            pm = phm,
            power = power,
            valid = valid,
            zregion_of_operation_MM = region_MM,
            zzgm_MM = gm_MM,
            zzids_MM = ids_MM,
            zzvds_MM = vds_MM,
            zzvgs_MM = vgs_MM
        )

        f.close()
        return results

    @classmethod
    def find_dc_gain(self, vout_diff):
        return np.abs(vout_diff)[0]

    @classmethod
    def find_ugbw(self, freq, vout_diff):
        gain = np.abs(vout_diff)
        ugbw, valid = self._get_best_crossing(freq, gain, val=1)
        if valid:
            return ugbw, valid
        else:
            return freq[0], valid

    @classmethod
    def find_phm(self, freq, vout):
        gain = np.abs(vout)
        phase = np.angle(vout, deg=True)
        phase = np.unwrap(np.deg2rad(phase))  # unwrap in radians
        phase = np.rad2deg(phase)

        phase_fun = interp.interp1d(freq, phase, kind='quadratic')
        ugbw, valid = self._get_best_crossing(freq, gain, val=1)

        if valid:
            # phase_at_ugbw wrapped into [-180, 180]
            phase_at_ugbw = (phase_fun(ugbw) + 180) % 360 - 180
            pm = 180 + phase_at_ugbw
            pm = (pm + 180) % 360 - 180   # final PM in [-180, 180]
            return pm
        else:
            return -180

    @classmethod
    def find_cmrr(self, vout_diff, vout_cm):
        gain_diff = self.find_dc_gain(vout_diff)
        gain_cm = np.abs(vout_cm)[0]

        return gain_diff / gain_cm

    @classmethod
    def extract_dc_sweep(self, results):
        """Extracts and returns sorted (dc_offsets, vouts) arrays from DC sweep results."""
        dc_offsets = []
        vouts = []

        for result in results.keys():
            if result.startswith('dcswp-'):
                val = results[result]["Voutp"]
                # Parse offset value from key string
                if result[6:10] == "1000":
                    dc_offset = int(result[6:10]) * 0.001 - 0.5
                else:
                    dc_offset = int(result[6:9]) * 0.001 - 0.5
                dc_offsets.append(dc_offset)
                vouts.append(val)

        # Sort both arrays by offset
        dc_offsets = np.array(dc_offsets)
        vouts = np.array(vouts)
        sort_idx = np.argsort(dc_offsets)

        return dc_offsets[sort_idx], vouts[sort_idx]

    @classmethod
    def find_vos(self, results, vcm):
        dc_offsets, vouts = self.extract_dc_sweep(results)

        # Create a smooth cubic spline across all points
        spline = interp.UnivariateSpline(dc_offsets, vouts, s=0)

        # Root function: difference between spline output and target Vcm
        def root_func(x):
            return spline(x) - vcm

        try:
            # Find zero-crossing of root_func (Vos)
            vos = sciopt.brentq(root_func, dc_offsets[0], dc_offsets[-1])
        except ValueError:
            vos = -1e2 # No valid crossing found in range

        return vos

    @classmethod
    def find_linearity(self, results, vout_diff, allowed_deviation_pct=2.0):
        gain = self.find_dc_gain(vout_diff)
        if gain < 1:
            # Gain too small, linearity undefined
            return None

        dc_offsets, vouts = self.extract_dc_sweep(results)

        # Fit spline
        spline = interp.UnivariateSpline(dc_offsets, vouts, s=0)

        # First derivative (slope)
        slope_spline = spline.derivative(n=1)

        # Define a fine resolution grid
        fine_x = np.linspace(dc_offsets.min(), dc_offsets.max(), 2000)
        fine_slope = slope_spline(fine_x)

        # Find index closest to x = 0
        zero_idx = np.argmin(np.abs(fine_x - 0))
        slope_at_zero = fine_slope[zero_idx]

        # Allowed deviation in slope
        allowed_dev = abs(slope_at_zero) * (allowed_deviation_pct / 100.0)

        # Expand left
        left_idx = zero_idx
        while left_idx > 0 and abs(fine_slope[left_idx] - slope_at_zero) <= allowed_dev:
            left_idx -= 1

        # Expand right
        right_idx = zero_idx
        while right_idx < len(fine_x) - 1 and abs(fine_slope[right_idx] - slope_at_zero) <= allowed_dev:
            right_idx += 1

        linear_range = (fine_x[left_idx], fine_x[right_idx])
        return linear_range

    @classmethod
    def find_output_voltage_swing(self, results, vcm, allowed_deviation_pct=10.0):
        # Extract sweep data
        dc_offsets, vouts = self.extract_dc_sweep(results)
        dc_offsets = np.array(dc_offsets)
        vouts = np.array(vouts)

        # Fit spline for smoothing
        spline = interp.UnivariateSpline(dc_offsets, vouts, s=0)

        # Derivative for slope
        slope_spline = spline.derivative()

        # Find Vos: offset where Vout is closest to vcm
        idx_vos = np.argmin(np.abs(vouts - vcm))
        vos = dc_offsets[idx_vos]

        # Max slope near Vos
        max_slope = slope_spline(vos)

        # Allowed slope deviation
        allowed_dev = abs(max_slope) * (allowed_deviation_pct / 100)

        # Walk outwards from Vos until slope deviation exceeds allowed_dev
        idx_left = idx_vos
        while idx_left > 0:
            if abs(slope_spline(dc_offsets[idx_left]) - max_slope) > allowed_dev:
                break
            idx_left -= 1

        idx_right = idx_vos
        while idx_right < len(dc_offsets) - 1:
            if abs(slope_spline(dc_offsets[idx_right]) - max_slope) > allowed_dev:
                break
            idx_right += 1

        # Get Y range
        y_min = vouts[idx_left]
        y_max = vouts[idx_right]

        return y_min, y_max
    
    @classmethod
    def find_integrated_noise(self, noise_results):
        """
        Integrate total noise PSD over frequency for all transistors starting with 'MM' and sum.

        Parameters:
        - noise_results: dict
            Keys: transistor names starting with 'MM'
            Values: numpy array of dict-like entries with noise PSD data per frequency point,
                    including key b'total' for total noise PSD at that frequency.

        Returns:
        - total_integrated_noise: float
            Total integrated noise power (V^2) summed across all transistors.
        """
        total_integrated_noise = 0.0

        # Fixed number of frequency points per transistor (given)
        num_points = 55

        # Frequency range: 1 MHz to 500 MHz (log-spaced, exactly 55 points)
        f_start = 1e6      # 1 MHz
        f_stop = 5e8       # 500 MHz
        freqs = np.logspace(np.log10(f_start), np.log10(f_stop), num_points)

        for key, noise_array in noise_results.items():
            if not key.startswith("MM"):
                continue

            # Check that the noise array length matches the expected 55 points
            if len(noise_array) != num_points:
                raise ValueError(f"Expected 55 points for {key}, but got {len(noise_array)}")

            # Extract total noise PSD values per frequency point
            total_psd = np.array([entry[b'total'] for entry in noise_array])

            # Integrate noise PSD vs frequency to get noise power (V^2)
            integrated_noise = scint.simps(total_psd, freqs)

            total_integrated_noise += integrated_noise

        return total_integrated_noise

    @classmethod
    def find_slew_rate(self, tran_results):
        time = np.array([t for t, _ in tran_results])
        vout = np.array([v for _, v in tran_results])

        # Create a spline interpolation of Vout vs time
        spline = interp.CubicSpline(time, vout)

        # Create a fine time grid for derivative evaluation
        time_fine = np.linspace(time[0], time[-1], 50000)

        # Calculate derivative (slope) at fine points
        dv_dt = spline.derivative()(time_fine)

        # Max absolute slope = slew rate
        slew_rate = np.max(np.abs(dv_dt))
        return slew_rate

    @classmethod
    def find_settle_time(self, tran_results, tol=0.005,
                        delay=1e-9, change=50e-12, width=100e-9):
        """
        Settling time measured from the input 50% point of the chosen edge
        to the first time Vout enters and stays within ±tol of its final value.
        edge = 'rise' (≈101.025 ns) for stimulus
        """

        time = np.array([t for t, _ in tran_results])
        vout = np.array([v for _, v in tran_results])

        # Spline interpolation of Vout vs time
        spline = interp.CubicSpline(time, vout)

        # Fine time grid for better resolution
        time_fine = np.linspace(time[0], time[-1], 50000)
        vout_fine = spline(time_fine)

        # Final value: average of last 5% of samples
        n_tail = max(5, len(vout_fine)//20)
        v_final = float(np.mean(vout_fine[-n_tail:]))

        lower, upper = v_final * (1 - tol), v_final * (1 + tol)

        # Check where Vout enters the ±tol band
        in_band = (vout_fine >= lower) & (vout_fine <= upper)
        stays_in = np.flip(np.cumprod(np.flip(in_band).astype(int)).astype(bool))
        idx = np.argmax(stays_in)

        if not stays_in[idx]:
            return None  # never settled

        t_out = time_fine[idx]

        # Fixed input 50% reference time
        t_ref = (delay + width + change/2) * 1e9  # 101.025 ns

        return max(0.0, t_out - t_ref)

    @classmethod
    def _get_best_crossing(self, xvec, yvec, val):
        interp_fun = interp.InterpolatedUnivariateSpline(xvec, yvec)

        def fzero(x):
            return interp_fun(x) - val

        xstart, xstop = xvec[0], xvec[-1]

        try:
            return sciopt.brentq(fzero, xstart, xstop), True
        except ValueError:
            return xstop, False

if __name__ == '__main__':

    yname = '/homes/natelgrw/Documents/titan_foundation_model/turbo_optimizer/working_current/eval_engines/specs_test/single_ended_cascode_current_mirror.yaml'
    eval_core = OpampMeasMan(yname)

    designs = eval_core.generate_data_set(n=1)
