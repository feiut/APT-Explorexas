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
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonArrayRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices

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

import java.util.*

class MapsActivity : AppCompatActivity(), OnMapReadyCallback {

    private lateinit var mMap: GoogleMap
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_maps)
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this::onMapReady)


//        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
//        getLastLocation()
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

        //Add a marker in Sydney and move the camera
        val current = LatLng(30.355, -97.752)

        mMap.addMarker(MarkerOptions().position(current).title("You are here!"))
        mMap.moveCamera(CameraUpdateFactory.newLatLng(current))
        getAllReports()
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(current,mMap.maxZoomLevel*0.85.toFloat()))
    }

    fun getAllReports(){
        val queue = Volley.newRequestQueue(this)
        val url = "http://apt-team7.appspot.com"
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
                txtHeader.text = "Failed to retrieve data"
                lstCategories.visibility = View.GONE
                Log.d("error", error.toString())
            }
            })
        queue.add(stringRequest)
    }
    fun bind(categories: JsonArray) {
//        Log.d("debug", categories.toString())
        for(category in categories){
            var categoryJson = JSONObject(category.toString()!!)
            var category_id = categoryJson.getString("cat_id")
            val queue = Volley.newRequestQueue(this)
            val cat_url: String = CategoryReportActivity.webUrl +"viewCategoryPost/" + category_id
            val jsonArrayRequest = JsonArrayRequest(Request.Method.GET, cat_url, null,
                Response.Listener<JSONArray> { response ->
                    CategoryReportActivity.reportContentList = response
                    for(reportIdx in 0 until CategoryReportActivity.reportContentList.length()) {
                        val report: JSONObject = CategoryReportActivity.reportContentList.getJSONObject(reportIdx)
                        var coordinate = report.getString("coordinates")
                        var latitude = coordinate.split(',')[0].subSequence(2,10).toString().toDouble()
                        var longitude = coordinate.split(',')[1].subSequence(1,10).toString().toDouble()
                        val current = LatLng(latitude, longitude)
                        mMap.addMarker(MarkerOptions()
                            .position(current)
                            .title("Report: " + report.getString("title"))
                            .snippet("Description: "+ report.getString("review")))
                    }
                },
                Response.ErrorListener { error->
                    Log.d("Error",error.toString())
                })
            queue.add(jsonArrayRequest)
        }

    }
//    @SuppressLint("MissingPermission")
//    private fun getLastLocation() {
//        fusedLocationClient.lastLocation.addOnSuccessListener {
//            it ?: return@addOnSuccessListener
//            handleLocation(it)
//        }
//    }
//
//    private fun handleLocation(location: Location) {
//        val geocoder = Geocoder(this, Locale.getDefault())
//        Thread(Runnable {
//            try {
//                var addresses = geocoder.getFromLocation(
//                    location.latitude, location.longitude, 1
//                )
//                var current = LatLng(location.latitude, location.longitude)
//                mMap.addMarker(MarkerOptions().position(current).title("You are here"))
//                mMap.moveCamera(CameraUpdateFactory.newLatLng(current))
//                mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(current,mMap.maxZoomLevel*2/3))
//                Log.i("TAG", addresses.first().toString())
//            } catch (e: Exception) {
//                e.printStackTrace()
//            }
//        }).start()
//    }
//
//    fun Context.hasPermissions(vararg permission: String): Boolean {
//        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) return true
//        return permission.all {
//            ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
//        }
//    }
//    fun Activity.requestPermissions(vararg permissions: String, requestCode: Int) {
//        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) return
//        this.requestPermissions(permissions, requestCode)
//    }
//    fun Activity.shouldShowCustomPermissionRequestHint(permission: String): Boolean {
//        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) return false
//        return !shouldShowRequestPermissionRationale(permission)
//    }
//    fun Context.LocationServiceEnable(): Boolean {
//        val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
//        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) ||
//                locationManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER)
//    }
//    fun Context.appSettingIntent(): Intent {
//        return Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
//            data = Uri.parse("package:$packageName")
//        }
//    }
//    fun LocationSettingIntent(): Intent {
//        return Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
//    }


}
