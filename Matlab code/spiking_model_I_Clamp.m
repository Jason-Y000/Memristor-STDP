% Hodgkin-Huxley Model for a neuron 
% Single input variable: V_k, voltage difference across membrane
% Single state variable: n
% Single output variable: i_k

% ---------------------------- Parameters --------------------------------
% Miscellaneous
dt = 0.01; % discrete timestep for updating the state
t = 0:dt:150; % 0-150ms w/ time step
V_0 = -65; % Rest potential of cell membrane is -65 mV 
V_out = 1:length(t);
V_out(1) = V_0;
C = 1; % Capacitance of 1 uF/cm^2

% Current clamped input
I_in = zeros(1,length(t));
I_in(50/dt:length(I_in)-50/dt) = 4; % Step current from 0 uA/cm^2 to 2 uA/cm^2

% Potassium parameters 
E_K = -12+V_0; % Potassium reversal potential (relative to V_0)
g_K_max = 36; % given as 36 mS/cm^2
I_K = 1:length(t);
g_K = 1:length(t);
n_K = 1:length(t);

[a_n,b_n] = stateParams_K(V_out(1),V_0); % Using V_0 asymptotic value
n_K(1) = a_n/(a_n+b_n); % Starting condition/state variable

% Sodium parameters
E_Na = 115+V_0; % Sodium reversal potential
g_Na_max = 120; % given as 120 mS/cm^2
I_Na = 1:length(t);
g_Na = 1:length(t);
m_Na = 1:length(t);
h_Na = 1:length(t);

[a_m,b_m] = stateParams_Na_m(V_out(1),V_0);
[a_h,b_h] = stateParams_Na_h(V_out(1),V_0);

m_Na(1) = a_m/(a_m+b_m);
h_Na(1) = a_h/(a_h+b_h);

% Leakage parameters
E_L = 10.6+V_0; % Leakage reversal potential
g_L = 0.3; % Given as 0.3 mS/cm^2
I_L = 1:length(t);


% -------------------------- Simulation ----------------------------------
for i = 1:length(t)-1 % calculating state-space system

    % Calculate voltage
    g_K(i) = g_K_max*(n_K(i)^4);
    g_Na(i)= g_Na_max*(m_Na(i)^3)*h_Na(i);

    % Calculate individual ionic currents
    I_Na(i) = g_Na(i)*(V_out(i)-E_Na);
    I_K(i) = g_K(i)*(V_out(i)-E_K);
    I_L(i) = g_L*(V_out(i)-E_L);

    % Calculating the new membrane potential
    V_out(i+1) = V_out(i) + (I_in(i) - (I_Na(i) + I_K(i) + I_L(i)))*(dt/C);
%     V_out(i+1) = V_out(i) + (I_in(i) - (I_Na(i) + I_L(i)))*(dt/C);

    % Updating state variables
    [a_n,b_n] = stateParams_K(V_out(i),V_0);
    [a_m,b_m] = stateParams_Na_m(V_out(i),V_0);
    [a_h,b_h] = stateParams_Na_h(V_out(i),V_0);

    n_K(i+1) = n_K(i) + (a_n*(1-n_K(i)) - b_n*n_K(i))*dt;
    m_Na(i+1) = m_Na(i) + (a_m*(1-m_Na(i)) - b_m*m_Na(i))*dt;
    h_Na(i+1) = h_Na(i) + (a_h*(1-h_Na(i)) - b_h*h_Na(i))*dt;
end

g_K(end) = g_K_max*(n_K(end)^4);
g_Na(end)= g_Na_max*(m_Na(end)^3)*h_Na(end);
I_Na(end) = g_Na(end)*(V_out(end)-E_Na);
I_K(end) = g_K(end)*(V_out(end)-E_K);
I_L(end) = g_L*(V_out(end)-E_L);

% ------------------------------ Plotting -------------------------------- 
figure
tiledlayout(1,3);
t1 = nexttile;
plot(t1, t(45/dt:end), V_out(45/dt:end));
title("Membrane Potential");
xlabel("Time (ms)");
ylabel("Voltage (mV)");
% ylim([-100,60]);

t2 = nexttile;
plot(t2, t(45/dt:end), I_K(45/dt:end));
xlabel("Time (ms)");
ylabel("Current (uA)");
title("Potassium Current");

t3 = nexttile;
plot(t3, t(45/dt:end), I_Na(45/dt:end));
xlabel("Time (ms)");
ylabel("Current(uA)");
title("Sodium Current");



