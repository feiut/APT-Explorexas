package com.example.phase3

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Build.VERSION_CODES.M
import androidx.appcompat.app.AppCompatActivity
import android.app.AlertDialog
import android.content.DialogInterface
import android.opengl.Visibility
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Spinner
import androidx.core.content.FileProvider
import kotlinx.android.synthetic.main.activity_create_report.*
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*

class CreateReportActivity : AppCompatActivity() {

    var currentPath:String? = null
    val TAKE_PICTURE = 1
    val SELECT_PICTURE = 2


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_create_report)
        successTextView.visibility = View.GONE
        val rating_spinner: Spinner = findViewById(R.id.submit_rating)
        // Create an ArrayAdapter using the string array and a default spinner layout

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
    }

    fun cancelCreateReport(){
        val intent = Intent(this, MenuActivity::class.java)
        startActivity(intent)
    }

    fun submitReport(){
        submit_title.visibility = View.GONE
        submit_category.visibility = View.GONE
        submit_place.visibility = View.GONE
        submit_review.visibility = View.GONE
        submit_rating.visibility = View.GONE
        submit_tag.visibility = View.GONE
        categoryTextView.visibility = View.GONE
        ratingTextView.visibility = View.GONE
        imageView.visibility = View.GONE
        buttonSubmit.visibility = View.GONE
        buttonCancel.visibility = View.GONE
        buttonGallery.visibility = View.GONE
        buttonCamera.visibility = View.GONE
        successTextView.visibility = View.VISIBLE
            // build alert dialog
//        val dialogBuilder = AlertDialog.Builder(this)
//
//        // set message of alert dialog
//        dialogBuilder.setMessage("Do you want to go back to homepage?")
//            // if the dialog is cancelable
//            .setCancelable(false)
//            // positive button text and action
//            .setPositiveButton("OK", DialogInterface.OnClickListener { dialogInterface: DialogInterface, i: Int ->
//                val intent = Intent(this, MainActivity::class.java)
//                startActivity(intent)
//            })
//            // negative button text and action
//            .setNegativeButton("Cancel", DialogInterface.OnClickListener {
//                    dialog, id -> dialog.cancel()
//            })
//
//        // create dialog box
//        val alert = dialogBuilder.create()
//        // set title for alert dialog box
//        alert.setTitle("New report created! ")
//        // show alert dialog
//        alert.show()
    }


    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if(requestCode == TAKE_PICTURE && resultCode == Activity.RESULT_OK){
            try{
                val file = File(currentPath as String)
                val uri = Uri.fromFile(file)
                imageView.setImageURI(uri)
            }catch (e: IOException){
                e.printStackTrace()
            }
        }
        if(requestCode == SELECT_PICTURE && resultCode == Activity.RESULT_OK){
            try{
                val uri = data!!.data
                imageView.setImageURI(uri)
            }catch (e: IOException){
                e.printStackTrace()
            }
        }
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


}
