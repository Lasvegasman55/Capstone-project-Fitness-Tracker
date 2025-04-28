// screens/NutritionScreen.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const NutritionScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Nutrition Screen Coming Soon</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: 18,
  },
});

export default NutritionScreen;