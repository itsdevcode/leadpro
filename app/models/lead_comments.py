from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, DateTime, ForeignKey, func
from app.core.database import Base
from app.models import user
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.lead import Lead

class LeadComment(Base):
    __tablename__ = "lead_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    lead: Mapped["Lead"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")