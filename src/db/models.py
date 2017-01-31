import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UniqueConstraint, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship, sessionmaker
from sqlalchemy import create_engine

global Base
Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    realm = Column(String(250), nullable=False)
    __table_args__ = (UniqueConstraint(name, realm, name='_name_realm_uc'),)

    def __repr__(self):
        return "<Player(name='{0}', realm='{1}')>".format(self.name, self.realm)

class Loot(Base):
    __tablename__ = "loot"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer) #actual ID of the item in-game
    #ilvl = Column(Integer, nullable=True) #ilvl of the item
    #socket = Column(Boolean, nullable=True) #whether the item has a socket
    instance = Column(Integer) #zone the item comes from
    #difficulty = Column(Integer) #difficulty the item dropped at
    #boss = Column(Integer) #ID of encounter item comes from

    def __repr__(self):
        return "<Loot(item_id='{0}', instance='{1}')>"\
            .format(self.item_id, self.instance)

class LootAward(Base):
    __tablename__ = "lootaward"
    id = Column(Integer, primary_key=True)
    reason = Column(Integer)
    date = Column(Date)
    item = Column(Integer, ForeignKey('loot.id'))
    replacement1 = Column(Integer, ForeignKey('loot.id'), nullable = True)
    replacement2 = Column(Integer, ForeignKey('loot.id'), nullable = True)
    replacements1 = relationship(Loot, foreign_keys=[replacement1])
    replacements2 = relationship(Loot, foreign_keys=[replacement2])
    player = Column(Integer, ForeignKey('player.id'))
    players = relationship(Player, foreign_keys=[player])

    def __repr__(self):
        return "<LootAward(item='{0}', reason='{1}', player='{2}')>".format(self.item, self.reason, self.player)


if __name__ == "__main__":
    engine = create_engine('sqlite:///deftools.db')
    Base.metadata.create_all(engine)
