prob_list = 1:52;
typelist = ['SMOOTH','NOISY3','NONDIFF','WILD3'];
ordolist = ['ior','ion','ioo','ion','iol','ios'];


% Compile le programme pour trouver x0
% !g++ -o generate_x0.exe generate_x0.cpp

% for np = 1 : 52
    
% end
np = 1;
[ifail,x0] = system(['generate_x0.exe ' num2str(np)]);
x0=str2num(x0)';
bounds=[-5, 5; -5 5;-5 5;-5 5;-5 5;-5 5;-5 5;-5 5;-5 5];
budget=1500;
[x,histout,comp]=imfil(x0,'bb',budget,bounds,imfil_optset());
histout(:,1:5)

