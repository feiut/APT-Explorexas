package com.example.phase3

import android.content.Intent
import android.graphics.Bitmap
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import android.widget.Button
import android.widget.ImageView
import kotlinx.android.synthetic.main.take_picture.*

class MainActivity : AppCompatActivity() {


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.take_picture)
//        var btnCamera: Button = findViewById (R.id.btnCamera)
//
//        btnCamera.setOnClickListener(View.OnClickListener {
//            fun onClick ( view : View ){
//                var intent: Intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
//                startActivityForResult(intent, 0)
//            }
//        })
    }

    fun btnOnClick(view:View){
        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        startActivityForResult(intent, 0)
    }

    @Override
    internal fun onActivityResult (requestCode : Int, resultCode : Int, data : Intent){
        super.onActivityResult(requestCode  , resultCode , data)
        val bitmap: Bitmap = data.extras?.get("data") as Bitmap
        val imageView: ImageView = findViewById(R.id.imageView)
        imageView.setImageBitmap(bitmap)
    }
}
