from typing import Any, TypeVar, Iterator, Iterable, Generic
import torch.nn as nn

class Module(nn.Module):
    def _forward_unimplemented(self, *input: Any) -> None:
        pass 
    def __init_subclass__(cls, **kwargs):
        if cls.__dict__.get('__call__', None) is None:
            return
        
        setattr(cls, 'forward', cls.__dict__['__call__'])
        delattr(cls, '__call__')

    @property
    def device(self):
        params = self.parameters()
        try:
            sample_param = next(params)
            return sample_param.device
        except StopIteration:
            raise RuntimeError(f"Unable to determine"
                               f" device of {self.__class__.__name__}") from None
        
M = TypeVar('M', bound=nn.Module)
T = TypeVar('T')

class TypedModuleList(nn.ModuleList, Generic[M]):
    def __getitem__(self, idx: int) -> M:
        return super().__getitem__(idx)
    
    def __setitem__(self, idx: int, module: M) -> None:
        return super().__setitem__(idx, module)
    
    def __iter__(self) -> Iterator[M]:
        return super().__iter__()
    
    def __iadd__(self: T, modules: Iterable[M]) -> T:
        return super().__iadd__(modules)
    
    def insert(self, index: int, module: M) -> None:
        return super().insert(index, module)
    
    def append(self: T, module: M) -> T:
        return super().append(module)
    
    def extend(self: T, modules: Iterable[M]) -> T:
        return super().extend(modules)
    
    def forward(self):
        raise NotImplementedError()
    

if __name__=='__main__':
    m = Module()
    print(m.device)