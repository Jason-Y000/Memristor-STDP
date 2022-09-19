files_in_this_folder = dir;
number_of_files = length(files_in_this_folder);
index = 3;
M = [];
for index = 3:number_of_files
    filename = files_in_this_folder(index).name;
    if strcmpi(filename(end-3:end), '.xls')
        data = xlsread(filename);
        I = data(:, 3);
        V = data(:, 2);
        C = [];
        for index = 42:182
            c = I(index)/V(index);
            C = [C;c];
        end
        maxCond = max(C);
        Iavg = mean(I(42:182));
        Vavg = mean(V(42:182));
        Cond = Iavg/Vavg;
        R = xlsread(filename, 'Calc', 'A1');
        N = str2num(filename(1:2));
        x = [N, R, Cond, maxCond];
        M = [M; x];
    end
end

dC = [0];
for index = 2:length(M)
    dc = M(index, 3) - M(index-1, 3);
    dC = [dC;dc];
end
M = [M, dC];

dW = [0];
for index = 2:length(M)
    dw = 100*M(index, 5)/M(index, 4);
    dW = [dW; dw];
end
M = [M, dW];

scatter(M(2:length(M),2), M(2:length(M),6), 'filled')
xlabel('\DeltaT (us)')
ylabel('\Deltaw (%)')
title('Block 3 Location (1, 1), 4V STDP Pulse')
grid on