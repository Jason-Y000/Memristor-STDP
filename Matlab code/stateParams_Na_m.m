function [a_m,b_m] = stateParams_Na_m(V, V_rest)
    a_m = (2.5-0.1*(V-V_rest))/(exp(2.5-0.1*(V-V_rest))-1);
    b_m = 4*exp((V_rest-V)/18);
end