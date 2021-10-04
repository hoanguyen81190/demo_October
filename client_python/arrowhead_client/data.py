from typing import Dict

from arrowhead_client.dto import DTOMixin


class BaseData(DTOMixin):
    bn: str 
    bt: int 
    bu: str
    bver: int 
    
    @classmethod 
    def make(
            cls,
            bn: str, 
            bt: int,
            bu: str,
            bver: int,
    ):
        return cls(
            bn=bn,
            bt=bt,
            bu=bu,
            bver=bver
    )
    
    @classmethod 
    def from_dto(cls, system_dto: Dict):
        return cls(
                bn=str(system_dto['bn']),
                bt=int(system_dto['bt']),
                bu=str(system_dto['bu']),
                bver=int(system_dto['bver'])
            )
    

class SensorData(DTOMixin):
    n: str
    t: float 
    u: str 
    v: float 
    vs: str
    vb: bool
    vd: str
    
    @classmethod 
    def make(
            cls,
            n: str,
            t: float,
            u: str, 
            v: float, 
            vs: str,
            vb: bool,
            vd: str,
    ):
        return cls(
            n=n,
            t=t,
            u=u, 
            v=v, 
            vs=vs,
            vb=vb,
            vd=vd,
        )
    
    @classmethod 
    def from_dto(cls, system_dto: Dict):
        return cls(
            n=str(system_dto['n']),
            t=float(system_dto['t']),
            u=str(system_dto['u']), 
            v=float(system_dto['v']), 
            vs=str(system_dto['vs']),
            vb=bool(system_dto['vb']),
            vd=str(system_dto['vd']),
        )
    
class Data(DTOMixin):
    bn: str 
    bs: int
    bt: int 
    bu: str
    bv: int
    bver: int
    n: str
    s: float 
    t: int 
    u: str 
    ut: int
    v: float
    vb: bool
    vd: str
    vs: str
    
    @classmethod 
    def make(
            cls,
            bn: str,
            bs: int,
            bt: int,
            bu: str,
            bv: int,
            bver: int,
            n: str,
            s: float,
            t: int,
            u: str,
            ut: int,
            v: float,
            vb: bool,
            vd: str,
            vs: str
            
    ):
        return cls(
            bn=bn,
            bs=bs,
            bt=bt,
            bu=bu,
            bv=bv,
            bver=bver,
            n=n,
            s=s,
            t=t,
            u=u,
            ut=ut,
            v=v,
            vb=vb,
            vd=vd,
            vs=vs
    )
    
    @classmethod 
    def from_dto(cls, system_dto: Dict):
        return cls(
                bn=str(system_dto['bn']),
                bs=int(system_dto['bs']),
                bt=int(system_dto['bt']),
                bu=str(system_dto['bu']),
                bv=int(system_dto['bv']),
                bver=int(system_dto['bver']),
                n=str(system_dto['n']),
                s=float(system_dto['s']),
                t=int(system_dto['t']),
                u=str(system_dto['u']),
                ut=int(system_dto['ut']),
                v=float(system_dto['v']),
                vb=bool(system_dto['vb']),
                vd=str(system_dto['vd']),
                vs=str(system_dto['vs'])
            )