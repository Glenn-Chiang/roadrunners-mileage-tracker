/* eslint-disable indent */
/* eslint-disable object-curly-spacing */
const { onRequest } = require("firebase-functions/v2/https");

const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");

initializeApp();

const db = getFirestore();

exports.registerCallsign = onRequest(async (req, res) => {
  try {
    const { userId, callsign } = req.query;
    const userDoc = db.collection("users").doc(userId);
    const result = await userDoc.set(
      {
        userId,
        callsign: callsign.toUpperCase(),
        totalMileage: 0,
      },
      { merge: true },
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error });
  }
});

exports.registerTeam = onRequest(async (req, res) => {
  try {
    const { userId, teamId } = req.query;
    const userDoc = db.collection("users").doc(userId);
    const result = await userDoc.set(
      {
        userId,
        teamId: teamId.toUpperCase(),
      },
      { merge: true },
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error });
  }
});

exports.clockMileage = onRequest(async (req, res) => {
  const { userId, mileage } = req.query;
  const userDoc = db.collection("users").doc(userId);
  await userDoc.update({
    totalMileage: FieldValue.increment(Number(mileage)),
  });
  const userDocSnap = await userDoc.get();
  const userData = userDocSnap.data();
  const totalMileage = userData.totalMileage;
  res.json({ totalMileage });
});

exports.getRanking = onRequest(async (req, res) => {
  try {
    const usersCollection = db.collection("users");
    const rankedUserDocs = await usersCollection
      .orderBy("totalMileage", "desc")
      .get();
    const rankedUsers = rankedUserDocs.docs.map((userDoc) => userDoc.data());
    res.json(rankedUsers);
  } catch (error) {
    res.status(500).json({ error: error });
  }
});

exports.getTeamRanking = onRequest(async (req, res) => {
  const teams = [];

  const teamIds = ["A", "B", "C"];
  try {
    for (const teamId of teamIds) {
      let teamMileage = 0;
      const teamMembersSnap = await db
        .collection("users")
        .where("teamId", "==", teamId)
        .orderBy("totalMileage", "desc")
        .get();
      const teamMembers = teamMembersSnap.docs.map((doc) => {
        const userData = doc.data();
        teamMileage += userData.totalMileage;
        return userData;
      });
      const team = { id: teamId, members: teamMembers, mileage: teamMileage };
      teams.push(team);
    }
    res.json(teams);
  } catch (error) {
    res.status(500).json({ error: error });
  }
});
