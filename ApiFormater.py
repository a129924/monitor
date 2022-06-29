from dataclasses import dataclass, field

@dataclass
class success_message:
    code:int=200
    message:str="Successed"
    status:bool=True
    result:dict[str:str]= field(default_factory=list)
    
@dataclass
class error_message: 
    code:int 
    message = "Successed"
    status:bool = False
    result:dict[str:str] = field(default_factory=list)
    
@dataclass
class sqlalchemy_Products:
    data:dict[str:str] = field(repr = False)
    ProductID:str = field(init=False)
    ProductName:str = field(init=False)
    Barcode:str = field(init=False)
    
    def __post_init__(self):
        self.ProductID = self.data["ProductID"]
        self.ProductName = self.data["ProductName"]
        self.Barcode = self.data["Barcode"]

@dataclass
class mongo_Product:
    data:list[dict] = field(repr = False)
    ProductID:str = field(init=False)
    ProductName:str = field(init=False)
    Barcode:str = field(init=False)
    
    def __post_init__(self):
        self.ProductID = self.data[0]["ProductID"]
        self.ProductName = self.data[0]["ProductName"]
        self.Barcode = self.data[0]["Barcode"]
