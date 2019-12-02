package com.example.phase3

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.location.Geocoder
import android.location.LocationManager
import android.os.Build
import android.content.Context
import android.content.pm.PackageManager
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.location.Location
import android.view.View
import android.widget.ListView
import android.widget.TextView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonArrayRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.google.android.gms.*
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions
import com.google.gson.JsonArray
import com.google.gson.JsonParser
import kotlinx.android.synthetic.main.activity_category_report.*
import kotlinx.android.synthetic.main.activity_view_categories.*
import org.json.JSONArray
import org.json.JSONObject
import com.google.android.gms.location.*
import android.Manifest
import android.os.Looper
import android.provider.Settings
import android.widget.Toast

import java.util.*

class MapsActivity : AppCompatActivity(), OnMapReadyCallback {

    private lateinit var mMap: GoogleMap
    var PERMISSION_ID = 42
    lateinit var mFusedLocationClient: FusedLocationProviderClient
    var thisLatitude = 37.7
    var thisLongitude = -97.1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        setContentView(R.layout.activity_maps)
        getLastLocation()
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this::onMapReady)
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
        getAllReports()
    }

    fun getAllReports(){
        val queue = Volley.newRequestQueue(this)
        val url = "http://apt-team7.appspot.com/mobile"
        val stringRequest = StringRequest(
            Request.Method.GET, url,
            Response.Listener {
                    response -> run {
                val parser = JsonParser()
                val jsonTree = parser.parse(response)
                val categories = jsonTree.asJsonArray
                bind(categories)
            }
            },
            Response.ErrorListener {
                    error -> run {
                txtHeader!!.text = "Failed to retrieve data"
                lstCategories.visibility = View.GONE
                Log.d("error", error.toString())
            }
            })
        queue.add(stringRequest)
    }
    fun bind(categories: JsonArray) {
        Log.d("debug", categories.toString())
        for(category in categories){
            var categoryJson = JSONObject(category.toString()!!)
            Log.d("debug", category.toString())
            var category_id = categoryJson.getString("cat_id")
            val queue = Volley.newRequestQueue(this)
            val cat_url: String = "http://apt-team7.appspot.com/viewCategoryPost/" + category_id
            val jsonArrayRequest = JsonArrayRequest(Request.Method.GET, cat_url, null,
                Response.Listener<JSONArray> { response ->
                    var reportContentList = response
                    for (reportIdx in 0 until reportContentList.length()) {
                        val report: JSONObject = reportContentList.getJSONObject(reportIdx)
                        Log.d("debug", report.toString())
                        var coordinate = report.getString("coordinates")
                        var latitude =
                            coordinate.split(',')[0].subSequence(2, 10).toString().toDouble()
                        var longitude =
                            coordinate.split(',')[1].subSequence(1, 10).toString().toDouble()
                        val current = LatLng(latitude, longitude)
                        mMap.addMarker(
                            MarkerOptions()
                                .position(current)
                                .title("Report: " + report.getString("title"))
                                .snippet("Description: " + report.getString("review"))
                        )
                    }
                },
                Response.ErrorListener { error->
                    Log.d("Error",error.toString())
                })
            queue.add(jsonArrayRequest)
        }

    }

    private fun checkPermissions(): Boolean {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
            ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED){
            return true
        }
        return false
    }

    private fun requestPermissions() {
        ActivityCompat.requestPermissions(
            this,
            arrayOf(
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.ACCESS_FINE_LOCATION
            ), PERMISSION_ID
        )
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        if (requestCode == PERMISSION_ID) {
            if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                // Granted. Start getting the location information
            }
        }
    }

    private fun isLocationEnabled(): Boolean {
        var locationManager: LocationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(
            LocationManager.NETWORK_PROVIDER
        )
    }

    @SuppressLint("MissingPermission")
    private fun getLastLocation() {
        if (checkPermissions()) {
            if (isLocationEnabled()) {
                mFusedLocationClient.lastLocation.addOnCompleteListener(this) { task ->
                    var location: Location? = task.result
                    if (location == null) {
                        requestNewLocationData()
                    } else {
//                        var current = LatLng(location.latitude, location.longitude)
                        var gps = GPSTracker(this)
                        var mlatitude = gps.getLatitude()
                        var mlongitude = gps.getLongitude()
                        var current = LatLng(mlatitude, mlongitude)
                        mMap.addMarker(MarkerOptions().position(current).title("You are here!"))
                        mMap.moveCamera(CameraUpdateFactory.newLatLng(current))
                        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(current,(mMap.minZoomLevel+mMap.maxZoomLevel)*3/4))
                    }
                }
            } else {
                Toast.makeText(this, "Turn on location", Toast.LENGTH_LONG).show()
                val intent = Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
                startActivity(intent)
            }
        } else {
            requestPermissions()
        }
    }

    @SuppressLint("MissingPermission")
    private fun requestNewLocationData() {
        var mLocationRequest = LocationRequest()
        mLocationRequest.priority = LocationRequest.PRIORITY_HIGH_ACCURACY
        mLocationRequest.interval = 0
        mLocationRequest.fastestInterval = 0
        mLocationRequest.numUpdates = 1

        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        mFusedLocationClient!!.requestLocationUpdates(
            mLocationRequest, mLocationCallback,
            Looper.myLooper()
        )
    }

    private val mLocationCallback = object : LocationCallback() {
        override fun onLocationResult(locationResult: LocationResult) {
            var mLastLocation: Location = locationResult.lastLocation
            Log.d("debug1", mLastLocation.latitude.toString())
            Log.d("debug1", mLastLocation.longitude.toString())
            thisLatitude = mLastLocation.latitude
            thisLongitude = mLastLocation.longitude
        }
    }

}
