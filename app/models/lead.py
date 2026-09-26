from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enum.lead import LeadStatus,LeadPriority

from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(String(250), nullable=True)
    status: Mapped[LeadStatus] = mapped_column(Enum(LeadStatus, name="lead_status_enum"), default=LeadStatus.NEW, nullable=False)
    priority: Mapped[LeadPriority] = mapped_column(Enum(LeadPriority, name="lead_priority_enum"), nullable=True)
    lead_source: Mapped[str | None] = mapped_column(String(50), nullable=True)
    next_follow_up: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    user: Mapped["User"] = relationship(back_populates="leads")