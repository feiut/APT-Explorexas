package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions

class MapsActivity : AppCompatActivity(), OnMapReadyCallback {

    private lateinit var mMap: GoogleMap

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_maps)
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap

        // Add a marker in Sydney and move the camera
        val current = LatLng(30.28, -97.734)
        val report1 = LatLng(30.28, -97.734)
        val report2 = LatLng(30.38, -97.736)
        val report3 = LatLng(30.35, -97.738)

        mMap.addMarker(MarkerOptions().position(current).title("You are here"))
        mMap.addMarker(MarkerOptions().position(report1).title("Report1"))
        mMap.addMarker(MarkerOptions().position(report2).title("Report2"))
        mMap.addMarker(MarkerOptions().position(report3).title("Report3"))
        mMap.moveCamera(CameraUpdateFactory.newLatLng(current))
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(current,mMap.maxZoomLevel*2/3))


    }
}
