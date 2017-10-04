function [fv,ifail,icount]=bb(x)
% La fonction à optimiser.

% Nom aléatoire pour un fichier
symbols = ['a':'z' 'A':'Z' '0':'9'];
MAX_ST_LENGTH = 10;
stLength = randi(MAX_ST_LENGTH)+6;
nums = randi(numel(symbols),[1 stLength]);
filename = symbols (nums);
filename = [filename '.txt'];

% xtest pour tester le print dans le pt.
% xtest = [1;2;3;4;5;6;7;8;9];

% Générer un fichier .txt avec le point x à l'interieur
fileID = fopen(filename,'w');
fprintf(fileID,'%d ',x');
fclose(fileID);

[ifail,fv] = system(['bb.exe ' filename]);
icount = 1;
fv = str2num(fv);
delete(filename)
end


%end