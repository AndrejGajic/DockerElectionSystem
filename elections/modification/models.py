from flask_sqlalchemy import SQLAlchemy


adminDb = SQLAlchemy()

class ElectionParticipant(adminDb.Model):
    __tablename__ = "electionparticipants"

    id = adminDb.Column(adminDb.Integer, primary_key=True)
    participantId = adminDb.Column(adminDb.Integer, adminDb.ForeignKey("participants.id"), nullable=False)
    electionId = adminDb.Column(adminDb.Integer, adminDb.ForeignKey("elections.id"), nullable=False)
    pollNumber = adminDb.Column(adminDb.Integer, nullable=False)  # ordinal number of candidate (participant) on election

    def __repr__(self):
        return self.id

class Participant(adminDb.Model):
    __tablename__ = "participants"

    id = adminDb.Column(adminDb.Integer, primary_key=True)
    name = adminDb.Column(adminDb.String(256), nullable=False)
    individual = adminDb.Column(adminDb.Boolean, nullable=False)  # True -> pojedinac ; False -> politicka stranka

    elections = adminDb.relationship("Election", secondary=ElectionParticipant.__table__, back_populates="participants")

    def __repr__(self):
        return str(self.id)


class Election(adminDb.Model):
    __tablename__ = "elections"

    id = adminDb.Column(adminDb.Integer, primary_key=True)
    start = adminDb.Column(adminDb.DateTime, nullable=False)
    end = adminDb.Column(adminDb.DateTime, nullable=False)
    individual = adminDb.Column(adminDb.Boolean, nullable=False)  # True -> pojedinacni; False -> politicki

    participants = adminDb.relationship("Participant", secondary=ElectionParticipant.__table__, back_populates="elections")
    votes = adminDb.relationship("Vote", back_populates="election")

    def __repr__(self):
        return self.id


class Vote(adminDb.Model):
    __tablename__ = "votes"

    id = adminDb.Column(adminDb.Integer, primary_key=True)
    electionId = adminDb.Column(adminDb.Integer, adminDb.ForeignKey("elections.id"), nullable=False)
    guid = adminDb.Column(adminDb.String(256), nullable=False)
    jmbg = adminDb.Column(adminDb.String(13), nullable = False)
    pollNumber = adminDb.Column(adminDb.Integer, nullable=False)
    valid = adminDb.Column(adminDb.Boolean, nullable=False)
    invalidReason = adminDb.Column(adminDb.String(256), nullable=True)

    election = adminDb.relationship("Election", back_populates="votes")

    def __repr__(self):
        return self.id

    def print(self):
        return f"{self.id} {self.electionId} {self.guid} {self.jmbg} {self.pollNumber} {self.valid} {self.invalidReason}"