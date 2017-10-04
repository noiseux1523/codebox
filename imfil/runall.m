prob_list = 1:52;
typelist = {'SMOOTH','NONDIFF','WILD3','NOISY3'};
typenum = containers.Map;
typenum('SMOOTH')=1;
typenum('NONDIFF')=2;
typenum('WILD3')=3;
typenum('NOISY3')=4;
ordolist = ['r','s','n','m','l','o'];
load('bound_data')
global ordo;

% Compile le programme pour trouver x0
% !g++ -o generate_x0.exe generate_x0.cpp
% for np = 1 : 52
%   for tp = 1 :4
% end
np = 1;
tp = 1;
type = typelist{tp};

% ici on trouve les bornes avec np et bound_data
iterator = 3;
a = [];

% On prends les valeurs existante dans la ligne de bound_data pour le prob
% correspondant
while isempty(bound_data{np+tp-1,iterator}) == false
    a = [a, str2num(bound_data{np+tp-1,iterator})];
    iterator = iterator +1;
end

% On prends la dimension
dim=length(a)/2;

% On prends le fix du log base 10 du plus grand entre la solution et le pt
% initial et on centre à 0.
bnds = 10^(fix(log10(max(abs(a))))+1);
bounds = zeros(dim,2);
bounds(:,1) = -bnds;
bounds(:,2) =bnds;

% Détermine le point de départ (redondant mais fait avant bounds)
[ifail,x0] = system(['generate_x0.exe ' num2str(np)]);
x0=str2num(x0)';

% Budget de 1500 comme NOMAD, à changer?
budget=1500;

%Roule l'algorithme avec case 1 = random
%ordo = 'o';
[x,histout,comp]=imfil(x0,'bb',budget,bounds,imfil_optset());

% Façon d'afficher les résultats pris de l'exemple 
histout(:,1:5)

