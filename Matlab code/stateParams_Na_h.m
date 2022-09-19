function [a_h,b_h] = stateParams_Na_h(V, V_rest)
    a_h = 0.07*exp((V_rest-V)/20);
    b_h = 1/(1+exp(3-0.1*(V-V_rest)));
end