clear all
clear 

% %--------------------------------------------------------------------------
% % For triangle waveforms
% % -------------------------------------------------------------------------
% N = 20;
% d = 0.01;
% % p1 = [0:0.1:1];
% % p2 = [0.9:-0.1:0];
% 
% V = [];
% 
% for i = 1:1:N
%     if mod(i,2) == 1
%         p1 = [0:0.1:0.9];
%         V = cat(2,V,p1);
%     
%     else
%         p2 = [1:-0.1:0.1];
%         V = cat(2,V,p2);
%     end
% end
% 
% 
% if mod(N,2) == 1
%     
%     V = [V,1];
% else
%     V = [V,0];
% end
% 
% [r,c] = size(V);
% 
% t = [0:d:(c-1)*d];
% 
% p = [t',V'];
% 
% % plot(p(:,1),p(:,2))
% % hold on
% %--------------------------------------------------------------------------
% % For Square waves
% %--------------------------------------------------------------------------
% N = 5; % Number of square pulses
% N_points = 20; % Number of points in each section of the square wave
% delta_t = 0.01; % Time spacing
% t_w = 0.01; % How much time the pulse is on
% t_o = 0.01; % How much time the pulse is off (t_w + t_o is one period)
% 
% V = [];
% 
% for i=1:1:5
%     [r,c] = size(0:(t_w)/(N_points-1):t_w);
%     V = cat(2,V,ones(1,c));
%     
%     [r,c] = size(0:(t_o)/(N_points-1):t_o);
%     V = cat(2,V,zeros(1,c));
% end
% V = [0,V];
% 
% t = [0:delta_t:(size(V,2)-1)*delta_t];
% p = [t',V'];
% 
% % plot(p(:,1),p(:,2))

%--------------------------------------------------------------------------
% For STDP waveforms
%--------------------------------------------------------------------------

delta_T = -9; % Time separating the pre- and postsynaptic spikes
V_start = 0; % Voltage starting amplitude 
V_max = 0.2; % Max value of the spike
V_min = -0.2; % Min value of the spike
N = 2000; % Number of points

% Define a presynaptic pulse spike

t0 = -8; % Time at which rising begins in us
t1 = -2; % Time of the first peak
t2 = 0; % Time of the second peak
t3 = 6; % Time to return to starting position 

p = []; % Points array
t = []; % Time points array
V = []; % All Voltage points array

m1 = (V_max-V_start)/(t1-t0); % Calculate slope of first line
b1 = V_max - m1*t1; % Find b of first line 
m2 = (V_min-V_max)/(t2-t1); % Calculate slope of second line
b2 = V_min - m2*t2; % Find b of second line
m3 = (V_start-V_min)/(t3-t2); % Calculate slope of third line 
b3 = V_start - m3*t3; % Find b of third line

syms x f(x)
f(x) = piecewise((t0<=x)&(x<t1),m1*x+b1,(t1<=x)&(x<t2),m2*x+b2,(t2<=x)&(x<=t3),m3*x+b3,V_start);

t = linspace(-50,50,N);
V = double(f(t));
p = [t',V'];

% Define a postsynaptic pulse spike

t0_prime = -35; % Time at which rising begins in us
t1_prime = -22; % Time of the first peak
t2_prime = -20; % Time of the second peak
t3_prime = -5; % Time to return to starting position 

p_prime = []; % Points array
t_prime = []; % Time points array
V_prime = []; % All Voltage points array

m1_prime = (V_max-V_start)/(t1_prime-t0_prime); % Calculate slope of first line
b1_prime = V_start - m1_prime*t0_prime; % Find b of first line 
m2_prime = (V_min-V_max)/(t2_prime-t1_prime); % Calculate slope of second line
b2_prime = V_min - m2_prime*t2_prime; % Find b of second line
m3_prime = (V_start-V_min)/(t3_prime-t2_prime); % Calculate slope of third line 
b3_prime = V_start - m3_prime*t3_prime; % Find b of third line

syms x g(x)
% g(x) = piecewise((t0_prime<=x)&(x<t1_prime),m1*x+b1_prime,(t1_prime<=x)&(x<t2_prime),m2*x+b2_prime,(t2_prime<=x)&(x<=t3_prime),m3*x+b3_prime,V_start);
g(x) = f(x-delta_T);

t_prime = linspace(-50,50,N);
V_prime = double(g(t_prime));
p_prime = [t_prime',V_prime'];

% Get output points as start channel voltage, end channel voltage, segment
% time
result_pre = [];
for i = 2:size(p,1)
    seg_time = p(i,1)-p(i-1,1);
    start_V = p(i-1,2);
    end_V = p(i,2);
    
    result_pre = cat(1,result_pre,[start_V,end_V,seg_time]);
end

result_post = [];
for i = 2:size(p_prime,1)
    seg_time = p_prime(i,1)-p_prime(i-1,1);
    start_V = p_prime(i-1,2);
    end_V = p_prime(i,2);
    
    result_post = cat(1,result_post,[start_V,end_V,seg_time]);
end

plot(p_prime(:,1),p_prime(:,2))
hold on
plot(p(:,1),p(:,2))
title("Sample STDP pre and post waveforms");
legend("Post","Pre",'Location','northeast');

% fplot(g(x));
% hold on
% fplot(f(x));
% % fplot(g(x)-f(x));
grid on;






