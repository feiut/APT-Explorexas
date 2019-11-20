package com.example.phase3

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.ImageDecoder
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Base64
import android.util.Log
import android.widget.*
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import com.android.volley.*
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.activity_create_report.*
import org.json.JSONArray
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*

class CreateReportActivity : AppCompatActivity() {

    var currentPath:String? = null
    val TAKE_PICTURE = 1
    val SELECT_PICTURE = 2
    val PERMISSION_REQUEST = 3
    private val UPLOAD_URL = "http://apt-team7.appspot.com/create_report"
    private var mClientAccountEmail: String? = null
    private var mTitle: EditText? = null
    private var mPlace: EditText? = null
    private var mReview: EditText? = null
    private var mTag: EditText? = null
    private var mCategory: Spinner? = null
    private var mRating: Spinner? = null
    private var mImage: ImageView? = null
    private var mlatitude: Double = 30.288478
    private var mlongitude: Double = -97.735104
    private var bitmap: Bitmap?= null
    private var mImageString:String ?= null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_create_report)
        val rating_spinner: Spinner = findViewById(R.id.submit_rating)
        // Create an ArrayAdapter using the string array and a default spinner layout
//        var ratingArray = arrayOf("0", "1", "2", "3", "4", "5")
//        var MyAdapter : ArrayAdapter<String> =  ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, ratingArray)
//********************
        val bundle = intent.extras
        mClientAccountEmail = bundle!!.getString("clientAccountEmail") as String
        Log.i("UserID", mClientAccountEmail)
        mTitle = findViewById(R.id.submit_title) as EditText
        mPlace = findViewById(R.id.submit_place) as EditText
        mReview = findViewById(R.id.submit_review) as EditText
        mTag = findViewById(R.id.submit_tag) as EditText
        mCategory = findViewById(R.id.submit_category) as Spinner
        mRating = findViewById(R.id.submit_rating) as Spinner
        mImage = findViewById(R.id.imageView) as ImageView

//**********************
        ArrayAdapter.createFromResource(
            this,
            R.array.report_rating,
            android.R.layout.simple_spinner_item
        ).also{ adapter ->
            // Specify the layout to use when the list of choices appears
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            // Apply the adapter to the spinner
            rating_spinner.adapter = adapter
        }
        val category_spinner: Spinner = findViewById(R.id.submit_category)
        ArrayAdapter.createFromResource(
            this,
            R.array.report_category,
            android.R.layout.simple_spinner_item
        ).also{ adapter ->
            // Specify the layout to use when the list of choices appears
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            // Apply the adapter to the spinner
            category_spinner.adapter = adapter
        }

        buttonGallery.setOnClickListener {
            dispatchGalleryIntent()
        }
        buttonCamera.setOnClickListener {
            dispatchCameraIntent()
        }
        buttonCancel.setOnClickListener {
            cancelCreateReport()
        }
        buttonSubmit.setOnClickListener {
            submitReport()
        }
        if(Build.VERSION.SDK_INT >= 23){
            if(!checkPermission()){
                requestPermission()
            }
        }
    }

    private fun checkPermission(): Boolean {
        var resultWrite:Int = ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
        var resultFineLocation:Int = ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
        var resultCoarseLocation:Int = ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION)
        if(resultWrite == PackageManager.PERMISSION_DENIED){
            Log.i("WRITE_PERMISSION", "DENIED")
            return false
        }
        if(resultFineLocation == PackageManager.PERMISSION_DENIED){
            Log.i("FineLocation_PERMISSION", "DENIED")
            return false
        }
        if(resultCoarseLocation == PackageManager.PERMISSION_DENIED){
            Log.i("CoarLocation_PERMISSION", "DENIED")
            return false
        }
        return true
    }

    private fun requestPermission(){
        ActivityCompat.requestPermissions(this, arrayOf(
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION),PERMISSION_REQUEST)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        when(requestCode){
            PERMISSION_REQUEST -> if (grantResults.size > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                Toast.makeText(this, "Prmission Granted", Toast.LENGTH_LONG).show()
            }else{
                Toast.makeText(this, "Permission denied", Toast.LENGTH_LONG).show()
            }
        }
    }

    fun cancelCreateReport(){
        val intent = Intent(this, MenuActivity::class.java)
        startActivity(intent)
    }

    fun submitReport(){
        var gps = GPSTracker(this)
        mlatitude = gps.getLatitude()
        mlongitude = gps.getLongitude()
        Log.i("LATITUDE", mlatitude.toString())
        Log.i("LONGITUDE", mlongitude.toString())

        val stringRequest = object: StringRequest(
            Method.POST,
            UPLOAD_URL,
            Response.Listener { response ->
                if(response.contains("success")){
                    Toast.makeText(this, "Image upload succeed", Toast.LENGTH_LONG).show()
                    imageView.setImageResource(R.drawable.ic_launcher_background)
                    submit_title.setText("")
                    submit_place.setText("")
                    submit_review.setText("")
                    submit_tag.setText("")
                    Log.i("Yeah!!!!!!1", response.toString())
                }else{
                    Toast.makeText(this, "response false 555 "+response.toString(), Toast.LENGTH_LONG).show()
                }
            },Response.ErrorListener { error ->
                Toast.makeText(this, "" + error, Toast.LENGTH_LONG).show()
                Log.i("ERROR!!!!!!1", error.toString())
            }){
            override fun getBodyContentType(): String {
                return "application/x-www-form-urlencoded; charset=UTF-8"
            }
            override fun getParams(): Map<String, String>{
                val params = HashMap<String, String>()
                params["email"] = mClientAccountEmail!!
                params["file"] = mImageString!!
                params["title"] = mTitle!!.text.toString()
                params["placeName"] = mPlace!!.text.toString()
                params["latitude"] = mlatitude.toString()
                params["longitude"] = mlongitude.toString()
                params["categoryName"] = mCategory!!.getSelectedItem().toString()
                params["review"] = mReview!!.text.toString()
                params["rating"] = mRating!!.getSelectedItem().toString()
                params["tagName"] = mTag!!.text.toString()
                return params
            }
        }
        stringRequest.setRetryPolicy(DefaultRetryPolicy(1000 * 10,
            DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT))
        Volley.newRequestQueue(this).add(stringRequest)

//        val intent = Intent(this, MenuActivity::class.java)
//        startActivity(intent)

    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if(requestCode == TAKE_PICTURE && resultCode == Activity.RESULT_OK){
            try{
                val file = File(currentPath as String)
                val uri = Uri.fromFile(file)
                getBitmapFromUri(uri)
//                set imageview by uri or bitmap
                imageView.setImageBitmap(bitmap)
//                imageView.setImageURI(uri)
            }catch (e: IOException){
                e.printStackTrace()
            }
        }
        if(requestCode == SELECT_PICTURE && resultCode == Activity.RESULT_OK){
            try{
                val uri = data!!.data
                getBitmapFromUri(uri!!)
                imageView.setImageURI(uri)
            }catch (e: IOException){
                e.printStackTrace()
            }
        }

        mImageString = getStringImage(bitmap!!)
    }

    fun dispatchGalleryIntent(){
        val intent = Intent()
        intent.type = "image/*"
        intent.action = Intent.ACTION_GET_CONTENT
        startActivityForResult(Intent.createChooser(intent, "select image"), SELECT_PICTURE)
    }

    fun dispatchCameraIntent(){
        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        var photoUri: Uri?= null
        if(intent.resolveActivity(packageManager)!= null){
            var photoFile: File?= null
            try{
                photoFile = createImage()
            }catch (e:IOException){
                e.printStackTrace()
            }
            if(photoFile != null){
                if(Build.VERSION.SDK_INT < Build.VERSION_CODES.N) {
                    photoUri = Uri.fromFile(photoFile)
                }else {
                    photoUri = FileProvider.getUriForFile(this,
                    "com.example.phase3.fileprovider", photoFile)
                }
                intent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri)
                startActivityForResult(intent, TAKE_PICTURE)
            }
        }
    }

    fun createImage(): File{
        val timeStamp = SimpleDateFormat("yyyMMdd_HHmmss").format(Date())
        val imageName = "JPEG_" + timeStamp
        var storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        var image = File.createTempFile(imageName, ".jpg", storageDir)
        currentPath = image.absolutePath
        return image
    }

    private fun getBitmapFromUri(uri:Uri){
//                transform image to bitmap
        if(Build.VERSION.SDK_INT < 28) {
            bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), uri)
        } else {
            val source = ImageDecoder.createSource(this.contentResolver, uri)
            bitmap = ImageDecoder.decodeBitmap(source)
        }
    }

    fun getStringImage(bitmap: Bitmap):String{
        var baos = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos)
        var b:ByteArray = baos.toByteArray()
        Log.i("ImageByteArray", b.toString())
        var temp:String = Base64.encodeToString(b, Base64.DEFAULT)
        Log.i("ImageString", temp)

        return temp
    }
    companion object {
        var webUrl:String = "http://apt-team7.appspot.com/"
        lateinit var currActivity: AppCompatActivity
        lateinit var reportContentList: JSONArray
    }
}
