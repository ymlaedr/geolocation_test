import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { GeolocationProperty } from '../templates/geolocation-template/geolocation-property';

@Injectable({
  providedIn: 'root'
})
export class GeolocationService {

  private position$: BehaviorSubject<GeolocationProperty> = new BehaviorSubject<GeolocationProperty>({});
  // private errors$: BehaviorSubject<GeolocationPositionError> = new BehaviorSubject<GeolocationPositionError>({
  //   code: 0, message: ''
  // });

  servePosition(): Observable<GeolocationProperty> {
    return this.position$.asObservable();
  }

  startWatchPosition(): Observable<any> {
    return new Observable((observer) => {
      let watchId: number;

      // Simple geolocation API check provides values to publish
      if ('geolocation' in navigator) {
        watchId = navigator.geolocation.watchPosition((position: GeolocationPosition) => {
          observer.next(position);
          this.position$.next({
            accuracy: position.coords.accuracy,
            altitude: position.coords.altitude,
            altitudeAccuracy: position.coords.altitudeAccuracy,
            heading: position.coords.heading,
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            speed: position.coords.speed,
            timestamp: position.timestamp,
          });
        }, (error: GeolocationPositionError) => {
          observer.error(error);
          // this.errors$.next(error);
          this.position$.next({});
        });
      } else {
        observer.error('Geolocation not available');
      }

      // When the consumer unsubscribes, clean up data ready for next subscription.
      return {
        unsubscribe() {
          navigator.geolocation.clearWatch(watchId);
        }
      };
    });
  }
}
