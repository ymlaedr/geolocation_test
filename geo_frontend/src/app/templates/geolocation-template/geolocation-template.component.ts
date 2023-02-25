import { Component, EventEmitter, Input, OnChanges, OnInit, Output } from '@angular/core';
import { GeolocationProperty } from './geolocation-property';

@Component({
  selector: 'app-geolocation-template',
  templateUrl: './geolocation-template.component.html',
  styleUrls: ['./geolocation-template.component.scss']
})
export class GeolocationTemplateComponent implements OnInit, OnChanges {

  @Input() position: GeolocationProperty | null = {};
  @Output() clickStartGeolocationWatch = new EventEmitter<void>();

  ngOnInit(): void {

  }

  ngOnChanges(): void {
    console.log(this.position);
  }

  onClickStartGeolocationWatch() {
    this.clickStartGeolocationWatch.emit();
  }
}
