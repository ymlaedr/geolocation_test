import { Component, OnDestroy, OnInit } from '@angular/core';
import { Observable, Subscription } from 'rxjs';
import { GeolocationService } from 'src/app/services/geolocation.service';
import { GeolocationProperty } from 'src/app/templates/geolocation-template/geolocation-property';

@Component({
  selector: 'app-geolocation-container',
  templateUrl: './geolocation-container.component.html',
  styleUrls: ['./geolocation-container.component.scss']
})
export class GeolocationContainerComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription = new Subscription();

  position$: Observable<GeolocationProperty>;

  constructor(private geolocationService: GeolocationService) {
    this.position$ = this.geolocationService.servePosition();
  }

  ngOnInit(): void {
  }

  startGeolocationWatch(): void {
    this.subscriptions.add(
      this.geolocationService.startWatchPosition().subscribe({
        next: (position: GeolocationPosition) => console.log(position),
        error: (error: GeolocationPositionError) => console.error(error),
      })
    )
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

}
