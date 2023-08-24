/* eslint-disable object-curly-spacing */
const { onRequest } = require("firebase-functions/v2/https");

const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");

initializeApp();

const db = getFirestore();

exports.registerUser = onRequest(async (req, res) => {
  try {
    const { userId, callsign } = req.query;
    const userDoc = db.collection("users").doc(userId);
    const result = await userDoc.set({
      userId,
      callsign,
      totalMileage: 0,
    });
    res.json(result);
  } catch (error) {
    res.json({ error: error });
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
