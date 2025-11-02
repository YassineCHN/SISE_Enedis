from pydantic import BaseModel

class InputFeatures(BaseModel):
    type_batiment: str
    periode_construction: str
    energie_chauffage: str
    surface_habitable_logement: float
    qualite_isolation_murs: str
    qualite_isolation_menuiseries: str
    zone_climatique: str
    classe_altitude: str
    logement_traversant: str

    # Champs manquants d'après le modèle :
    annee_construction: int
    type_energie_principale_chauffage: str
    classe_inertie_batiment: str
