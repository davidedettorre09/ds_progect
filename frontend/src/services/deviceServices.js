import axiosInstance from "./axiosConfig";

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL_DEVICE;

/**
 * @returns {Object} - The server response with data
 * @throws Will throw an error if it fails.
 */
const getAllDevices = async () => {
  try {
    const response = await axiosInstance.get(`${BASE_API_URL}/devices/`);
    return response.data;
  } catch (error) {
    console.error("Error in fetching devices!", error);
    throw error;
  }
};

/**
 * @returns {Object} - The server response with data
 * @throws Will throw an error if it fails.
 */
const getAllClientDevices = async () => {
    try {
      const response = await axiosInstance.get(`${BASE_API_URL}/my-devices/`);
      return response.data;
    } catch (error) {
      console.error("Error in fetching Client devices!", error);
      throw error;
    }
  };

/**
 * @param {string} deviceId - The device's identifier
 * @returns {Object} - The server response with data
 * @throws Will throw an error if it fails.
 */

const getSingleDevice = async (deviceId) => {
    try {
      const response = await axiosInstance.get(`${BASE_API_URL}/devices/${deviceId}/`);
      return response.data;
    } catch (error) {
      console.error("Error in fetching the device!", error);
      throw error;
    }
  };


/**
 * @param {Object} deviceData - An object containing device data
 * @returns {Object} - The server response with data
 * @throws Will throw an error if it fails.
 */
const createDevice = async (deviceData) => {
  try {
    const response = await axiosInstance.post(`${BASE_API_URL}/devices/`, deviceData);
    return response.data;
  } catch (error) {
    console.error("Error creating the device!", error);
    throw error;
  }
};

/**
 * @param {Object} deviceData - An object containing device data
 * @param {string} deviceId - The device's identifier
 * @returns {Object} - The server response with data 
 * @throws Will throw an error if it fails.
 */
const updateDevice = async (deviceData, deviceId) => {
    try {
      const response = await axiosInstance.put(`${BASE_API_URL}/devices/${deviceId}/`, deviceData);
      return response.data;
    } catch (error) {
      console.error("Error creating the device!", error);
      throw error;
    }
  };

  /**
 * @param {string} deviceId - The device's identifier
 * @returns {Object} - The server response with data 
 * @throws Will throw an error if it fails.
 */
const deleteDevice = async (deviceId) => {
    try {
      const response = await axiosInstance.delete(`${BASE_API_URL}/devices/${deviceId}/`);
      return response.data;
    } catch (error) {
      console.error("Error creating the device!", error);
      throw error;
    }
  };



export default {
  getAllDevices,
  getSingleDevice,
  createDevice,
  updateDevice,
  getAllClientDevices,
  deleteDevice,
};