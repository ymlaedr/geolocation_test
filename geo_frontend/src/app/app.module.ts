import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GeolocationService } from './services/geolocation.service';
import { GeolocationContainerComponent } from './containers/geolocation-container/geolocation-container.component';
import { GeolocationTemplateComponent } from './templates/geolocation-template/geolocation-template.component';

@NgModule({
  declarations: [
    AppComponent,
    GeolocationContainerComponent,
    GeolocationTemplateComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
  ],
  providers: [
    GeolocationService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
