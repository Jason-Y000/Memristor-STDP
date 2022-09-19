% Hodgkin-Huxley Model for a neuron 
% Single input variable: V_k, voltage difference across membrane
% Single state variable: n
% Single output variable: i_k

% ---------------------------- Parameters --------------------------------
% Miscellaneous
dt = 0.001; % discrete timestep for updating the state
t = 0:dt:10; % 0-150ms w/ time step
V_0 = -65; % Rest potential of cell membrane is -65 mV 
I_out = 1:length(t); % Current will be measured in uA/cm^2

% Capacitive current 
C_m = 1; % Capacitance of 1 uF/cm^2
I_C = 1:length(t);

% Voltage clamped input
V_in = zeros(1,length(t));
% V_in(50/dt:length(I_out)) = 100; % Voltage in mV
V_in(1:2/dt) = -65; % Voltage in mV
V_in(2/dt+1:6/dt-1) = 100;
V_in(6/dt:length(t)) = -65;

% Potassium parameters 
E_K = -12+V_0; % Potassium reversal potential (relative to V_0)
g_K_max = 36; % given as 36 mS/cm^2
I_K = 1:length(t);
g_K = 1:length(t);
n_K = 1:length(t);

[a_n,b_n] = stateParams_K(V_in(1),V_0); % Using V_0 asymptotic value
n_K(1) = a_n/(a_n+b_n); % Starting condition/state variable

% Sodium parameters
E_Na = 115+V_0; % Sodium reversal potential
g_Na_max = 120; % given as 120 mS/cm^2
I_Na = 1:length(t);
g_Na = 1:length(t);
m_Na = 1:length(t);
h_Na = 1:length(t);

[a_m,b_m] = stateParams_Na_m(V_in(1),V_0);
[a_h,b_h] = stateParams_Na_h(V_in(1),V_0);

m_Na(1) = a_m/(a_m+b_m);
h_Na(1) = a_h/(a_h+b_h);

% Leakage parameters
E_L = 10.6+V_0; % Leakage reversal potential
g_L = 0.3; % Given as 0.3 mS/cm^2
I_L = 1:length(t);


% -------------------------- Simulation ----------------------------------
for i = 1:length(t) % calculating state-space system

    % Calculate conductance
    g_K(i) = g_K_max*(n_K(i)^4);
    g_Na(i)= g_Na_max*(m_Na(i)^3)*h_Na(i);

    % Calculate individual current contributions
    I_Na(i) = g_Na(i)*(V_in(i)-E_Na);
    I_K(i) = g_K(i)*(V_in(i)-E_K);
    I_L(i) = g_L*(V_in(i)-E_L);
    
    if i == length(t)
        I_C(i) = 0;
    else
        I_C(i) = C_m*(V_in(i+1)-V_in(i))/dt; % Approximate derivative with slope
    end

    % Calculating the resulting current
    I(i) = I_Na(i)+I_K(i)+I_L(i)+I_C(i);

    % Updating state variables
    [a_n,b_n] = stateParams_K(V_in(i),V_0);
    [a_m,b_m] = stateParams_Na_m(V_in(i),V_0);
    [a_h,b_h] = stateParams_Na_h(V_in(i),V_0);
    
    n_K(i+1) = n_K(i) + (a_n*(1-n_K(i)) - b_n*n_K(i))*dt;
    m_Na(i+1) = m_Na(i) + (a_m*(1-m_Na(i)) - b_m*m_Na(i))*dt;
    h_Na(i+1) = h_Na(i) + (a_h*(1-h_Na(i)) - b_h*h_Na(i))*dt;
end

% ------------------------------ Plotting -------------------------------- 
figure
tiledlayout(2,2);
t1 = nexttile;
% plot(t1, t(45/dt:end), g_K(45/dt:end));
plot(t1, t, g_K);
title("Conductance of Potassium");
xlabel("Time (ms)");
ylabel("Conductance (mS/cm^2)");
% xlim([t(50/dt),t(50/dt)+15]);
% ylim([0,40]);
% 
% t2 = nexttile;
% plot(t2, t(45/dt:end), g_Na(45/dt:end));
% xlabel("Time (ms)");
% ylabel("Conductance (mS/cm^2)");
% title("Conductance of Sodium");
% xlim([t(50/dt),t(50/dt)+15]);
% ylim([0,50]);

% t1 = nexttile;
% plot(t1, t, I_K);
% title("Potassium Current");
% xlabel("Time (ms)");
% ylabel("Current (uA/cm^2)");

t2 = nexttile;
plot(t2, t, I_Na);
xlabel("Time (ms)");
ylabel("Current (uA/cm^2)");
title("Sodium Current");

t3 = nexttile;
plot(t3, t, V_in);
xlabel("Time (ms)");
ylabel("Voltage");
title("Voltage");

t4 = nexttile;
plot(t4, t, I_K+I_Na);
xlabel("Time (ms)");
ylabel("Ionic Current");
title("Current");



