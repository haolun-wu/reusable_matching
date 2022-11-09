fname = 'normal_and_pjt';


val = csvread(strcat(strcat('vals_', fname), '.csv'));
I = csvread(strcat(strcat('I_', fname), '.csv'))+1;
J = csvread(strcat(strcat('J_', fname), '.csv'))+1;

b = csvread(strcat(strcat('b_', fname), '.csv'));
c = csvread(strcat(strcat('c_', fname), '.csv'));


A = sparse(I,J, val);
options = optimoptions(@linprog,'Display', 'iter')
[x, fval] = linprog(-c,A,b,[], [], zeros(size(c)), ones(size(c)), [], options);

csvwrite(strcat(strcat('LPval_', fname), '.csv'), fval);
csvwrite(strcat(strcat('X_', fname), '.csv'), x);
