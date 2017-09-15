function[out]=ior(in)
% This is random ordering
    [~,n] = size(in);
    out = in(:,randperm(n));
end