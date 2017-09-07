function[out]=ior(in,complete)
% This is random ordering
    [~,n] = size(in);
    out = in(:,randperm(n));
end