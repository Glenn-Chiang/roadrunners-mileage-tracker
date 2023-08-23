const { logger } = require("firebase-functions");
const { onRequest } = require("firebase-functions/v2/https");
const { onDocumentCreated } = require("firebase-functions/v2/firestore");

const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");

initializeApp();

const db = getFirestore();

exports.registerUser = onRequest(async (req, res) => {
  const { userId, callsign } = req.query;
  const userDoc = db.collection("users").doc(userId);
  const result = await userDoc.set({
    userId,
    callsign,
    totalMileage: 0,
  });
  res.json(result);
});

exports.addMileage = onRequest(async (req, res) => {
  const { userId, mileage } = req.query;
  const userDoc = db.collection("users").doc(userId);
  await userDoc.update({
    totalMileage: FieldValue.increment(Number(mileage)),
  });
  const userDocSnap = await userDoc.get();
  const userData = userDocSnap.data();
  const totalMileage = userData.totalMileage;
  res.json({totalMileage});
});
