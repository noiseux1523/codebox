function[out]=ordo2(in)
% This is random ordering
    [~,n] = size(in);
    out = in(:,randperm(n));
end