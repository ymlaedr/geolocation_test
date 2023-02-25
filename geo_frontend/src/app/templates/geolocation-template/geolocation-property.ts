export interface GeolocationProperty {
  accuracy?: number;
  altitude?: number | null;
  altitudeAccuracy?: number | null;
  heading?: number | null;
  latitude?: number;
  longitude?: number;
  speed?: number | null;
  timestamp?: EpochTimeStamp;
}
