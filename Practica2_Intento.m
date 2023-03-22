system("anchurDef.py");

% Abrir el archivo en modo de lectura
fid = fopen('tree.txt', 'r');
tline = fgetl(fid);
while ischar(tline)
    disp(tline)
    tline = fgetl(fid);
end
fclose(fid);


fid = fopen('solution.txt', 'r');
tline = fgetl(fid);
while ischar(tline)
    disp(tline)
    tline = fgetl(fid);
end
fclose(fid);