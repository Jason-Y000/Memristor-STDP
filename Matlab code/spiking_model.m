% Using state-space system representation of potassium-ion channel action
% potentials. Specific parameters from Biolek/Kolka 2013 using tuned
% Hodgkin-Huxley model.

% Single input variable: V_k, voltage difference across membrane
% Single state variable: n
% Single output variable: i_k

timestep = 1e7; % discrete timestep for updating the state
f = 100; % 100 Hz
E_k = 12e-3; % mV membrane potential for K
g_k = 36e-3; % given as 36 mS/cm^2
t = 0:1/timestep:1; % 0-1s w/ time step
V_k = (0.005+0.005*sawtooth(2*pi*f*t, 1/2))+12e-3; % sin(f*2*pi*t);
i_k = 1:timestep+1;

u = 100*(V_k+E_k)+1;
a_n = 100*u./(exp(u)-1); % parameters from Biolek/Kolka, changes tilt of curve
b_n = 125*exp(12.5*(V_k+E_k)); % same as above
n = 0; % Starting condition/state variable

% If you want to read in data to compare this is how you do it
%m = xlsread("../DataProcessing/eb2_data/IVcurve_1_16_1.xls");

% Introduction of stochastic condition: Gaussian, binomial
% Not currently being used in the model though
gauss_rand = 1;
block = 0;
P_f = 0.6;

for i = 1:timestep+1 % calculating state-space system
    if block == 1
          i_k(i) = g_k; % refractory period, ignore for now
    else
        i_k(i) = g_k*n^4*(V_k(i)-E_k); % HH equation for K
    end

    n = (n+(a_n(i)*(1-n)-b_n(i)*n)/timestep); % state-equation for n
end

% All of this code was reading from data files, ignore for now until
% you have your own proper data files

% t_vec = m(:,1);
% i_vec = m(:,4);
% v_vec = m(:,3)*1000;
% 
% t_vec1 = t(1:timestep/f);
% i_vec1 = i_k(1:timestep/f);
% v_vec1 = V_k(1:1e5);
% 
% t_vec2 = t(timestep/f+1:2*timestep/f);
% i_vec2 = i_k(timestep/f+1:2*timestep/f);
% v_vec2 = V_k(1e5+1:2e5);
% 
% t_vec3 = t(2*timestep/f+1:3*timestep/f);
% i_vec3 = i_k(2*timestep/f+1:3*timestep/f);
% v_vec3 = V_k(2e5+1:3e5);
% 
% t_vec4 = t(3*timestep/f+1:4*timestep/f);
% i_vec4 = i_k(3*timestep/f+1:4*timestep/f);
% v_vec4 = V_k(3e5+1:4e5);


% Plotting code
% Can plot the data by cycles or the simulations


figure
tiledlayout(1,2);
t1 = nexttile;
plot(t1, V_k(timestep/2:timestep)*1000, i_k(timestep/2:timestep)*1000);
title("Steady-State I-V Curve");
xlabel("Voltage (mV)");
ylabel("Current (mA)");
t2 = nexttile;

% This code was plotting each cycle of the data
%plot(t_vec1, i_vec1, 'color', 'g');
%xlabel("Time(s)");
%ylabel("Current (nA)");
%ylim([0 50]);
%xlim([0 200]);
%hold on
%plot(t_vec2, i_vec2, 'color', 'r');
%hold on
%plot(t_vec3, i_vec3, 'color', 'm');
%hold on
%plot(t_vec4, i_vec4, 'color', 'b');
%legend({"Cycle 1", "Cycle 2", "Cycle 3", "Cycle 4"},'Location', 'northwest');
%hold off

title("Full I-V Curve");
plot(t2, t(1:1*timestep/f)*1000, V_k(1:1*timestep/f)*1000);
xlabel("Time (ms)");
ylabel("Voltage (mV)");
title("Applied Voltage");
% t4 = nexttile;
% plot(t4, t(1:1*timestep/f)*1000, i_k(1:1*timestep/f)*1000);
% xlabel("Time (ms)");
% ylabel("Current (nA)");
% title("Resultant Current");
% % 
% figure
% plot(t(1:9*timestep/f)/timestep*1000, i_k(1:9*timestep/f)*1000);
% xlabel("Time (ms)");
% ylabel("Current (mA)");
% title("Resultant Current");