package com.example.phase3

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Build.VERSION_CODES.M
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
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
        buttonGallery.setOnClickListener {
            dispatchGalleryIntent()
        }
        buttonCamera.setOnClickListener {
            dispatchCameraIntent()
        }
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
        if(intent.resolveActivity(packageManager)!= null){
            var photoFile: File?= null
            try{
                photoFile = createImage()
            }catch (e:IOException){
                e.printStackTrace()
            }
            if(photoFile != null){
                var photoUri = FileProvider.getUriForFile(this,
                    "com.example.phase3.fileprovider", photoFile)
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
