function [a_n,b_n] = stateParams_K(V,V_rest)
    a_n = (0.1-0.01*(V-V_rest))/(exp(1-0.1*(V-V_rest))-1);
    b_n = 0.125*exp((V_rest-V)/80);
end