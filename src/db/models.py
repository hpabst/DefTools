import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UniqueConstraint, Date, VARCHAR, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship, sessionmaker
from sqlalchemy import create_engine

global Base
Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    realm = Column(VARCHAR, nullable=False)
    wow_class = Column(Integer)
    __table_args__ = (UniqueConstraint(name, realm, name='_name_realm_uc'),)

    def __repr__(self):
        return "<Player(name='{0}', realm='{1}')>".format(self.name, self.realm)


class Loot(Base):
    __tablename__ = "loot"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer) #actual ID of the item in-game
    name = Column(VARCHAR, default="Unknown")
    instance = Column(Integer) #zone the item comes from
    bonus_ids = relationship("BonusID")

    def __repr__(self):
        return "<Loot(item_id='{0}', instance='{1}')>"\
            .format(self.item_id, self.instance)

class BonusID(Base):
    __tablename__ = "bonusid"
    id = Column(Integer, primary_key=True)
    bonus_id = Column(Integer)
    loot_parent = Column(Integer, ForeignKey("loot.id"))



    def __repr__(self):
        return "BonusID(bonus_id='{0}', id_effect='{1}')>".format(self.bonus_id, self.id_effect)


class LootAward(Base):
    __tablename__ = "lootaward"
    id = Column(Integer, primary_key=True)
    reason = Column(VARCHAR)
    award_date = Column(Date)
    item = Column(Integer, ForeignKey('loot.id'))
    item_rel = relationship(Loot, foreign_keys=[item])
    replacement1 = Column(Integer, ForeignKey('loot.id'), nullable = True)
    replacement2 = Column(Integer, ForeignKey('loot.id'), nullable = True)
    replacement1_rel = relationship(Loot, foreign_keys=[replacement1])
    replacement2_rel = relationship(Loot, foreign_keys=[replacement2])
    player = Column(Integer, ForeignKey('player.id'))
    player_rel = relationship(Player, foreign_keys=[player])

    def __repr__(self):
        return "<LootAward(item='{0}', reason='{1}', player='{2}')>".format(self.item, self.reason, self.player)


def create_db():
    engine = create_engine('sqlite:///deftools.db')
    Base.metadata.create_all(engine)
    return

if __name__ == "__main__":
    create_db()
