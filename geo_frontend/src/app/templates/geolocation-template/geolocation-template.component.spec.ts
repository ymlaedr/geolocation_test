import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeolocationTemplateComponent } from './geolocation-template.component';

describe('GeolocationTemplateComponent', () => {
  let component: GeolocationTemplateComponent;
  let fixture: ComponentFixture<GeolocationTemplateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GeolocationTemplateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GeolocationTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
